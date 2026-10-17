"""Ejecuta un archivo .js en la pestaña de TradingView de un Brave/Chrome abierto con
--remote-debugging-port, mediante el protocolo CDP, y guarda el resultado en un archivo
(sin usar el portapapeles).

El archivo se ejecuta en el marco superior de la pestaña (Runtime.evaluate, contexto por
defecto). Dentro del script, `copy(x)` guarda x como salida (en vez de ir al portapapeles) y
`console.log/error/warn/info` se recogen en una lista. Si el script devuelve un valor
distinto de undefined, también se usa como salida. Solo se conecta a 127.0.0.1.

Ejemplos:
    python tools/cdp_ejecutar.py --listar
    python tools/cdp_ejecutar.py tools/devtools_volcar_plots.js -o manual/plots_lite_1016_1630_1700.json
    python tools/cdp_ejecutar.py tools/devtools_volcar_metainfo.js -o manual/metainfo_X.json

Requiere: pip install websockets
"""
import argparse
import asyncio
import json
import sys
import urllib.request
from pathlib import Path

try:
    import websockets
except ImportError:
    sys.exit("Falta el paquete 'websockets': pip install websockets")


def listar_pestañas(puerto):
    with urllib.request.urlopen(f"http://127.0.0.1:{puerto}/json", timeout=5) as r:
        return [t for t in json.load(r) if t.get("type") == "page"]


def elegir_pestaña(puerto, filtro_url):
    pestañas = listar_pestañas(puerto)
    candidatas = [t for t in pestañas if filtro_url in t.get("url", "")]
    if not candidatas:
        urls = "\n".join(f"  - {t.get('url')}" for t in pestañas) or "  (ninguna)"
        sys.exit(f"No hay ninguna pestaña con '{filtro_url}' en la URL. Pestañas abiertas:\n{urls}")
    if len(candidatas) > 1:
        print(f"Aviso: {len(candidatas)} pestañas coinciden; se usa la primera: {candidatas[0]['url']}",
              file=sys.stderr)
    return candidatas[0]


def envolver(codigo):
    """Envuelve el JS para capturar copy() y console.*. Primero como expresión (permite
    esperar una promesa/IIFE); si no es una expresión, como cuerpo de instrucciones."""
    cabecera = (
        "(async function(){\n"
        "  const __logs = []; let __copiado;\n"
        "  const copy = (x) => { __copiado = x; };\n"
        "  const __fmt = (a) => { try { return typeof a === 'string' ? a : JSON.stringify(a); } catch (e) { return String(a); } };\n"
        "  const console = { log: (...a) => __logs.push(['log', a.map(__fmt).join(' ')]),\n"
        "                    info: (...a) => __logs.push(['info', a.map(__fmt).join(' ')]),\n"
        "                    warn: (...a) => __logs.push(['warn', a.map(__fmt).join(' ')]),\n"
        "                    error: (...a) => __logs.push(['error', a.map(__fmt).join(' ')]) };\n"
    )
    cierre = (
        "  return { devuelto: __devuelto === undefined ? null : __devuelto, copiado: __copiado === undefined ? null : __copiado, logs: __logs };\n"
        "})()"
    )
    cuerpo = codigo.rstrip()
    while cuerpo.endswith(";"):
        cuerpo = cuerpo[:-1].rstrip()
    como_expresion = cabecera + "  const __devuelto = await (\n" + cuerpo + "\n);\n" + cierre
    como_cuerpo = cabecera + "  let __devuelto;\n" + codigo + "\n" + cierre
    return como_expresion, como_cuerpo


async def evaluar(ws_url, expresion, tiempo_max):
    async with websockets.connect(ws_url, max_size=None) as ws:
        await ws.send(json.dumps({
            "id": 1, "method": "Runtime.evaluate",
            "params": {"expression": expresion, "awaitPromise": True, "returnByValue": True,
                       "timeout": int(tiempo_max * 1000)},
        }))
        while True:
            msg = json.loads(await ws.recv())
            if msg.get("id") == 1:
                return msg


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("js", nargs="?", help="archivo .js a ejecutar")
    ap.add_argument("-o", "--salida", help="archivo donde guardar el resultado (JSON o texto)")
    ap.add_argument("--puerto", type=int, default=9222)
    ap.add_argument("--filtro-url", default="tradingview.com/chart", help="subcadena de la URL de la pestaña")
    ap.add_argument("--tiempo-max", type=float, default=60, help="segundos máximos de ejecución")
    ap.add_argument("--sobrescribir", action="store_true", help="permitir sobrescribir la salida")
    ap.add_argument("--listar", action="store_true", help="solo lista las pestañas y sale")
    args = ap.parse_args()

    try:
        if args.listar:
            for t in listar_pestañas(args.puerto):
                print(f"{t.get('url')}  |  {t.get('title')}")
            return
        if not args.js or not args.salida:
            ap.error("hacen falta el archivo .js y --salida")
        salida = Path(args.salida)
        if salida.exists() and not args.sobrescribir:
            sys.exit(f"{salida} ya existe; usa otro nombre o --sobrescribir (las exportaciones no se editan).")
        codigo = Path(args.js).read_text(encoding="utf-8")
        pestaña = elegir_pestaña(args.puerto, args.filtro_url)
        print(f"Pestaña: {pestaña['url']}", file=sys.stderr)
        expr_a, expr_b = envolver(codigo)
        msg = asyncio.run(evaluar(pestaña["webSocketDebuggerUrl"], expr_a, args.tiempo_max))
        exc = msg.get("result", {}).get("exceptionDetails")
        if exc and "SyntaxError" in json.dumps(exc):
            msg = asyncio.run(evaluar(pestaña["webSocketDebuggerUrl"], expr_b, args.tiempo_max))
            exc = msg.get("result", {}).get("exceptionDetails")
    except OSError as e:
        sys.exit(f"No se pudo conectar al puerto {args.puerto}: {e}. ¿Brave abierto con --remote-debugging-port?")

    if "error" in msg:
        sys.exit(f"Error CDP: {msg['error']}")
    if exc:
        sys.exit("Excepción en la página: " + (exc.get("exception", {}).get("description") or exc.get("text", "")))
    res = msg["result"]["result"].get("value") or {}
    for nivel, texto in res.get("logs", []):
        print(f"[{nivel}] {texto[:2000]}", file=sys.stderr)
    contenido = res.get("copiado") if res.get("copiado") is not None else res.get("devuelto")
    if contenido is None:
        sys.exit("El script no produjo salida (ni copy() ni valor devuelto); no se escribe nada.")
    if not isinstance(contenido, str):
        contenido = json.dumps(contenido, ensure_ascii=False)
    try:  # si es JSON válido, se guarda con sangría legible
        contenido = json.dumps(json.loads(contenido), ensure_ascii=False, indent=1) if len(contenido) < 5_000_000 else contenido
    except ValueError:
        pass
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(contenido, encoding="utf-8", newline="\n")
    print(f"Guardado {salida} ({len(contenido)} caracteres)", file=sys.stderr)


if __name__ == "__main__":
    main()
