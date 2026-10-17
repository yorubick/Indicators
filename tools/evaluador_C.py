"""Evaluador de reglas de selección de C (PoiSzn EMA Origin Lite).

Mide si una regla predice el C oficial, separando lo que se ajustó de lo que se
predijo y comparando siempre con líneas base y con el azar.

Garantías de diseño:
  * Las reglas reciben un `Caso` con solo lo que el indicador puede ver:
    resolución de la fuente (dt), número inclusivo de barras (n), duración
    transcurrida T = END - START y las velas OHLCV de START a END. No reciben
    identificador, fecha ni hora, así que no pueden codificar casos a mano.
  * Las reglas con parámetros se evalúan con validación cruzada que deja fuera
    un grupo cada vez (grupo = mismo START y misma dt). Los casos de un grupo
    comparten casi todas sus velas y no pueden repartirse entre ajuste y prueba.
  * Cada resultado se compara con una prueba de permutación: cuántos aciertos
    exactos se obtendrían por azar barajando los C medidos con la misma dt.

Uso (desde la raíz del repositorio):
  python tools/evaluador_C.py evaluar [--conjuntos maestro,2m] [--reglas a,b] [--json salida.json]
  python tools/evaluador_C.py registrar --ohlcv velas.json --start 2026-10-16T14:30:00Z \
      --end 2026-10-16T15:00:00Z --dt 60 [--reglas a,b] [--nota "..."]
  python tools/evaluador_C.py verificar --archivo experimentos/predicciones/<id>.json --C 87

`registrar` escribe la predicción en experimentos/predicciones/. Hay que hacer
commit de ese archivo ANTES de leer el C oficial en TradingView; si no, no
cuenta como predicción ciega.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "master_all_C_cases.json"
PREDICCIONES = ROOT / "experimentos" / "predicciones"
MINTICK = 0.25  # NQ
N_FRONTERA = 21
PERMUTACIONES = 2000


# ---------------------------------------------------------------------------
# Casos
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Vela:
    o: float
    h: float
    l: float
    c: float
    v: float


@dataclass(frozen=True)
class Caso:
    """Lo único que ve una regla."""
    dt: int            # segundos de la fuente
    n: int             # barras inclusivas de START a END
    T: int             # END - START en segundos
    velas: tuple[Vela, ...]

    @property
    def T_inclusivo(self) -> int:
        return self.n * self.dt


@dataclass(frozen=True)
class Registro:
    caso: Caso
    C: float           # C oficial medido
    id: str
    grupo: str

    @property
    def largo(self) -> bool:
        return self.caso.n >= N_FRONTERA


def cargar_maestro(path: Path = MASTER) -> list[Registro]:
    data = json.loads(path.read_text(encoding="utf-8"))
    registros = []
    for c in data["cases"]:
        if c["C_measurement_kind"] != "Lite_decimal_verified":
            continue
        velas = tuple(Vela(b["open"], b["high"], b["low"], b["close"], b["volume"]) for b in c["OHLCV"])
        dt = int(c["source_seconds"])
        T = int(c["END_unix"] - c["START_unix"])
        n = T // dt + 1
        if n != c["bars"] or len(velas) != n:
            raise ValueError(f"caso {c['id']}: n={n}, bars={c['bars']}, velas={len(velas)}")
        registros.append(Registro(Caso(dt, n, T, velas), float(c["C_Lite"]), c["id"], f"{c['START']}|{dt}"))
    return registros


# Casos de 2 m leídos en vivo (CDP) el 14/15-oct y fijados en
# tools/tabla_maestra_12_casos_2m.py. No están en el maestro y no tienen CSV de
# curvas en manual/: son evidencia secundaria. Se usaron para ajustar la κ del
# clon Pine, así que para esa regla son datos de ajuste, no de control.
CASOS_2M = [
    ("12oct_1430_1510", "data/ohlcv_2m_1430_1516.json", 0, 21, 124),
    ("12oct_1430_1512", "data/ohlcv_2m_1430_1516.json", 0, 22, 153),
    ("12oct_1430_1514", "data/ohlcv_2m_1430_1516.json", 0, 23, 146),
    ("12oct_1430_1516", "data/ohlcv_2m_1430_1516.json", 0, 24, 190),
    ("14oct_1400_1444", "data/ohlcv_2m_14oct_1400_1454.json", 0, 23, 181),
    ("14oct_1400_1446", "data/ohlcv_2m_14oct_1400_1454.json", 0, 24, 191),
    ("14oct_1400_1448", "data/ohlcv_2m_14oct_1400_1454.json", 0, 25, 128),
    ("14oct_1400_1450", "data/ohlcv_2m_14oct_1400_1454.json", 0, 26, 191),
    ("14oct_1400_1452", "data/ohlcv_2m_14oct_1400_1454.json", 0, 27, 195),
    ("14oct_1400_1454", "data/ohlcv_2m_14oct_1400_1454.json", 0, 28, 177),
    ("14oct_1402_1450", "data/ohlcv_2m_14oct_1400_1454.json", 1, 25, 128),
]


def cargar_2m() -> list[Registro]:
    registros = []
    for ident, archivo, desde, n, C in CASOS_2M:
        filas = json.loads((ROOT / archivo).read_text(encoding="utf-8"))[desde:desde + n]
        if len(filas) != n:
            raise ValueError(f"{ident}: {len(filas)} velas, se esperaban {n}")
        velas = tuple(Vela(b["open"], b["high"], b["low"], b["close"], b["volume"]) for b in filas)
        registros.append(Registro(Caso(120, n, (n - 1) * 120, velas), float(C), ident, f"{ident[:10]}|120"))
    return registros


# Mediciones nuevas del 16-17 oct (EXP-20261016-dependencias): C exacto del Lite
# recuperado de las exportaciones de manual/ (fuente = gráfico con
# tools/invertir_C_csv.py; fuente más fina con tools/invertir_C_subfuente.py).
# Velas de la fuente descargadas con el conector de TradingView. Ninguna se usó
# para construir las reglas existentes.
_EXP = "experimentos/EXP-20261016-dependencias/"
CASOS_NUEVOS = [
    ("20261016_1640_1700_60s", _EXP + "NQ1_1m_2026-10-15_16.json", "2026-10-16T16:40", "2026-10-16T17:00", 60, 88),
    ("20261012_1331_1353_60s", _EXP + "NQ1_1m_2026-10-12_13.json", "2026-10-12T13:31", "2026-10-12T13:53", 60, 89),
    ("20261016_1645_1700_60s", _EXP + "NQ1_1m_2026-10-15_16.json", "2026-10-16T16:45", "2026-10-16T17:00", 60, 60),
    ("20261016_1645_1700_30s", _EXP + "NQ1_30s_2026-10-15_16.json", "2026-10-16T16:45", "2026-10-16T17:00", 30, 47),
    ("20261016_1645_1700_15s", _EXP + "NQ1_15s_2026-10-16_0900_2059.json", "2026-10-16T16:45", "2026-10-16T17:00", 15, 40),
    ("20261016_1645_1700_5s", _EXP + "NQ1_5s_2026-10-16_1400_1800.json", "2026-10-16T16:45", "2026-10-16T17:00", 5, 82),
    ("20261016_1645_1700_1s", _EXP + "NQ1_1s_2026-10-16_1644_1730.json", "2026-10-16T16:45", "2026-10-16T17:00", 1, 73),
    ("20261016_1640_1700_30s", _EXP + "NQ1_30s_2026-10-15_16.json", "2026-10-16T16:40", "2026-10-16T17:00", 30, 86),
    ("20261016_1640_1700_15s", _EXP + "NQ1_15s_2026-10-16_0900_2059.json", "2026-10-16T16:40", "2026-10-16T17:00", 15, 85),
]


def cargar_nuevos() -> list[Registro]:
    """La vela END del gráfico (1 m) incluye todas sus subvelas de la fuente."""
    registros = []
    for ident, archivo, start, end, dt, C in CASOS_NUEVOS:
        b = json.loads((ROOT / archivo).read_text(encoding="utf-8"))["bars"]
        ts = int(datetime.fromisoformat(start + ":00+00:00").timestamp())
        te = int(datetime.fromisoformat(end + ":00+00:00").timestamp()) + 60 - dt
        velas = tuple(Vela(o, h, l, c, v) for t, o, h, l, c, v in zip(b["t"], b["o"], b["h"], b["l"], b["c"], b["v"]) if ts <= t <= te)
        n = (te - ts) // dt + 1
        # En fuentes de segundos faltan las subvelas sin operaciones; tampoco
        # existen para el indicador (la inversión de C con estos datos da residuo 0).
        if len(velas) != n and not (dt < 15 and len(velas) >= 0.99 * n):
            raise ValueError(f"{ident}: {len(velas)} velas, se esperaban {n}")
        registros.append(Registro(Caso(dt, n, te - ts, velas), float(C), ident, f"{start}|{dt}"))
    return registros


CONJUNTOS = {"maestro": cargar_maestro, "2m": cargar_2m, "nuevos": cargar_nuevos}


# ---------------------------------------------------------------------------
# Reglas
# ---------------------------------------------------------------------------

def redondeo_pine(x: float) -> int:
    """math.round de Pine: empate hacia arriba (para x >= 0)."""
    return math.floor(x + 0.5)


def C_corto(caso: Caso) -> float:
    """Régimen corto (resultado R2): exacto en 35/35 casos del maestro."""
    return max(caso.dt, caso.T_inclusivo * 10.0 / 183.0)


Regla = Callable[[Caso], float]
# Una regla ajustable recibe los registros de ajuste y devuelve una Regla.
ReglaAjustable = Callable[[list[Registro]], Regla]


def base_T_transcurrido(caso: Caso) -> float:
    if caso.n < N_FRONTERA:
        return C_corto(caso)
    return redondeo_pine(caso.T / 18.3)


def base_T_inclusivo(caso: Caso) -> float:
    if caso.n < N_FRONTERA:
        return C_corto(caso)
    return redondeo_pine(caso.T_inclusivo / 18.3)


def pine_v1_3_auto(caso: Caso) -> float:
    """Traducción del modo Auto de pine/PoiSzn_EMA_Origin_Lite_v1_3_OpenSource.pine
    (harmonic_k = 0, gráfico = fuente). Variables de la caja START..END inclusive."""
    if caso.n < N_FRONTERA:
        return C_corto(caso)
    if caso.n == N_FRONTERA:
        return 125.0
    hi = max(v.h for v in caso.velas)
    lo = min(v.l for v in caso.velas)
    rango = max(MINTICK, hi - lo)
    fin = caso.velas[-1]
    close_pos = (fin.c - lo) / rango
    eficiencia = min(1.0, abs(fin.c - caso.velas[0].o) / rango)
    kappa = 18.30 - eficiencia * (18.30 - 14.80)
    if close_pos >= 0.95 or close_pos <= 0.05:
        kappa = 14.80
    elif eficiencia < 0.20:
        kappa = 17.23
    return float(redondeo_pine(caso.T / kappa))


def ajustar_kappa_por_dt(entrenamiento: list[Registro]) -> Regla:
    """round(T/κ_dt), con κ_dt = mediana de T/C en los casos largos de ajuste."""
    por_dt: dict[int, list[float]] = defaultdict(list)
    for r in entrenamiento:
        if r.largo:
            por_dt[r.caso.dt].append(r.caso.T / r.C)
    todos = [k for ks in por_dt.values() for k in ks]
    kappas = {dt: statistics.median(ks) for dt, ks in por_dt.items()}
    k_global = statistics.median(todos) if todos else 18.3

    def regla(caso: Caso) -> float:
        if caso.n < N_FRONTERA:
            return C_corto(caso)
        return redondeo_pine(caso.T / kappas.get(caso.dt, k_global))
    return regla


def ajustar_mediana_por_n(entrenamiento: list[Registro]) -> Regla:
    """Mediana del C medido en los casos de ajuste con la misma dt y el n más cercano."""
    tabla: dict[int, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
    for r in entrenamiento:
        if r.largo:
            tabla[r.caso.dt][r.caso.n].append(r.C)

    def regla(caso: Caso) -> float:
        if caso.n < N_FRONTERA:
            return C_corto(caso)
        filas = tabla.get(caso.dt)
        if not filas:
            return base_T_transcurrido(caso)
        n_cercano = min(filas, key=lambda n: (abs(n - caso.n), n))
        return redondeo_pine(statistics.median(filas[n_cercano]))
    return regla


REGLAS_FIJAS: dict[str, Regla] = {
    "base_T_transcurrido": base_T_transcurrido,
    "base_T_inclusivo": base_T_inclusivo,
    "pine_v1_3_auto": pine_v1_3_auto,
}
REGLAS_AJUSTABLES: dict[str, ReglaAjustable] = {
    "kappa_por_dt": ajustar_kappa_por_dt,
    "mediana_por_n": ajustar_mediana_por_n,
}
DESCRIPCION = {
    "base_T_transcurrido": "línea base: corto exacto; largo round(T/18.3)",
    "base_T_inclusivo": "línea base: corto exacto; largo round(n·dt/18.3)",
    "pine_v1_3_auto": "modo Auto del clon Pine v1.3 (κ por eficiencia, n=21→125)",
    "kappa_por_dt": "ajustada: round(T/κ) con κ por dt (validación cruzada)",
    "mediana_por_n": "ajustada: mediana de C por (dt, n) cercano (validación cruzada)",
}


# ---------------------------------------------------------------------------
# Evaluación
# ---------------------------------------------------------------------------

def acierta(pred: float, medido: float, largo: bool) -> bool:
    if largo:
        return redondeo_pine(pred) == round(medido)
    return abs(pred - medido) < 1e-6


def predecir(nombre: str, registros: list[Registro]) -> list[float]:
    if nombre in REGLAS_FIJAS:
        regla = REGLAS_FIJAS[nombre]
        return [regla(r.caso) for r in registros]
    ajustar = REGLAS_AJUSTABLES[nombre]
    preds = [0.0] * len(registros)
    grupos = sorted({r.grupo for r in registros})
    for g in grupos:
        regla = ajustar([r for r in registros if r.grupo != g])
        for i, r in enumerate(registros):
            if r.grupo == g:
                preds[i] = regla(r.caso)
    return preds


def permutacion(preds: list[float], registros: list[Registro], semilla: int = 20261016) -> tuple[float, float]:
    """Aciertos exactos esperados por azar (largo) barajando C dentro de cada dt; y p-valor."""
    idx = [i for i, r in enumerate(registros) if r.largo]
    observados = sum(acierta(preds[i], registros[i].C, True) for i in idx)
    por_dt: dict[int, list[int]] = defaultdict(list)
    for i in idx:
        por_dt[registros[i].caso.dt].append(i)
    rng = random.Random(semilla)
    conteos = []
    for _ in range(PERMUTACIONES):
        total = 0
        for ids in por_dt.values():
            medidos = [registros[i].C for i in ids]
            rng.shuffle(medidos)
            total += sum(acierta(preds[i], m, True) for i, m in zip(ids, medidos))
        conteos.append(total)
    p = (1 + sum(c >= observados for c in conteos)) / (1 + PERMUTACIONES)
    return statistics.mean(conteos), p


def resumir(nombre: str, preds: list[float], registros: list[Registro]) -> dict:
    largos = [i for i, r in enumerate(registros) if r.largo]
    cortos = [i for i, r in enumerate(registros) if not r.largo]
    err = [abs(redondeo_pine(preds[i]) - round(registros[i].C)) for i in largos]
    azar, p = permutacion(preds, registros)
    por_dt = {}
    for dt in sorted({registros[i].caso.dt for i in largos}):
        ids = [i for i in largos if registros[i].caso.dt == dt]
        por_dt[dt] = f"{sum(acierta(preds[i], registros[i].C, True) for i in ids)}/{len(ids)}"
    return {
        "regla": nombre,
        "descripcion": DESCRIPCION.get(nombre, ""),
        "corto_exactos": f"{sum(acierta(preds[i], registros[i].C, False) for i in cortos)}/{len(cortos)}",
        "largo_exactos": sum(acierta(preds[i], registros[i].C, True) for i in largos),
        "largo_total": len(largos),
        "largo_exactos_por_dt": por_dt,
        "largo_azar_medio": round(azar, 1),
        "largo_p_valor": round(p, 4),
        "largo_a_2s": sum(e <= 2 for e in err),
        "largo_mediana_error_s": statistics.median(err) if err else None,
        "largo_media_error_s": round(statistics.mean(err), 2) if err else None,
        "predicciones": [
            {"id": r.id, "dt": r.caso.dt, "n": r.caso.n, "C": r.C, "pred": round(preds[i], 6),
             "acierto": acierta(preds[i], r.C, r.largo)}
            for i, r in enumerate(registros)
        ],
    }


def tabla(registros: list[Registro], nombres: list[str], titulo: str) -> list[dict]:
    resultados = [resumir(n, predecir(n, registros), registros) for n in nombres]
    n_largo = resultados[0]["largo_total"]
    print(f"== {titulo}: {len(registros)} casos ({len(registros) - n_largo} cortos, {n_largo} largos); "
          f"{len({r.grupo for r in registros})} grupos START|dt")
    print(f"{'regla':<22} {'corto':>7} {'largo exacto':>13} {'azar':>6} {'p':>7} {'±2 s':>6} {'med.err':>8}  por dt")
    for res in resultados:
        print(f"{res['regla']:<22} {res['corto_exactos']:>7} "
              f"{res['largo_exactos']:>6}/{res['largo_total']:<6} {res['largo_azar_medio']:>6} "
              f"{res['largo_p_valor']:>7} {res['largo_a_2s']:>6} {res['largo_mediana_error_s']:>8}  "
              f"{res['largo_exactos_por_dt']}")
    print()
    return resultados


def cmd_evaluar(args: argparse.Namespace) -> None:
    nombres = args.reglas.split(",") if args.reglas else [*REGLAS_FIJAS, *REGLAS_AJUSTABLES]
    salida = {}
    for conjunto in args.conjuntos.split(","):
        salida[conjunto] = tabla(CONJUNTOS[conjunto](), nombres, conjunto)
    print("'azar' = aciertos exactos esperados barajando los C medidos dentro de cada dt; "
          "p = probabilidad de igualar o superar el resultado por azar.")
    if args.json:
        Path(args.json).write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"detalle por caso: {args.json}")


# ---------------------------------------------------------------------------
# Predicciones registradas (controles ciegos)
# ---------------------------------------------------------------------------

def leer_velas(path: Path) -> list[dict]:
    """Acepta el formato del conector de TradingView (filas o columnas) o una lista de filas."""
    data = json.loads(path.read_text(encoding="utf-8"))
    bars = data.get("bars", data) if isinstance(data, dict) else data
    if isinstance(bars, dict):  # columnas
        return [dict(t=t, o=o, h=h, l=l, c=c, v=v)
                for t, o, h, l, c, v in zip(bars["t"], bars["o"], bars["h"], bars["l"], bars["c"], bars["v"])]
    return [dict(t=b.get("t", b.get("time")), o=b.get("o", b.get("open")), h=b.get("h", b.get("high")),
                 l=b.get("l", b.get("low")), c=b.get("c", b.get("close")), v=b.get("v", b.get("volume")))
            for b in bars]


def a_unix(texto: str) -> int:
    return int(datetime.fromisoformat(texto.replace("Z", "+00:00")).timestamp())


def commit_actual() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "desconocido"


def cmd_registrar(args: argparse.Namespace) -> None:
    start, end, dt = a_unix(args.start), a_unix(args.end), int(args.dt)
    if (end - start) % dt:
        sys.exit("END - START debe ser múltiplo de dt")
    filas = sorted((b for b in leer_velas(Path(args.ohlcv)) if start <= b["t"] <= end), key=lambda b: b["t"])
    n = (end - start) // dt + 1
    esperadas = list(range(start, end + 1, dt))
    if [b["t"] for b in filas] != esperadas:
        faltan = sorted(set(esperadas) - {b["t"] for b in filas})
        sys.exit(f"faltan {len(faltan)} velas de {n} en la ventana (primera: {faltan[:1]})")
    caso = Caso(dt, n, end - start, tuple(Vela(b["o"], b["h"], b["l"], b["c"], b["v"]) for b in filas))
    registros = cargar_maestro()
    nombres = args.reglas.split(",") if args.reglas else [*REGLAS_FIJAS, *REGLAS_AJUSTABLES]
    preds = {}
    for nombre in nombres:
        regla = REGLAS_FIJAS.get(nombre) or REGLAS_AJUSTABLES[nombre](registros)
        preds[nombre] = round(regla(caso), 6)
    ventana = json.dumps(filas, sort_keys=True).encode()
    ident = f"{datetime.fromtimestamp(start, timezone.utc):%Y%m%d_%H%M%S}_{datetime.fromtimestamp(end, timezone.utc):%H%M%S}_{dt}s"
    destino = PREDICCIONES / f"{ident}.json"
    if destino.exists():
        sys.exit(f"ya existe {destino.relative_to(ROOT)}; no se sobrescriben predicciones")
    registro = {
        "id": ident,
        "simbolo": args.simbolo,
        "START": datetime.fromtimestamp(start, timezone.utc).isoformat(),
        "END": datetime.fromtimestamp(end, timezone.utc).isoformat(),
        "dt": dt, "n": n, "T": end - start,
        "regimen": "largo" if n >= N_FRONTERA else "corto",
        "predicciones": preds,
        "registrado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "commit_base": commit_actual(),
        "velas_sha256": hashlib.sha256(ventana).hexdigest(),
        "velas": filas,
        "nota": args.nota or "",
        "resultado": None,
    }
    PREDICCIONES.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(registro, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"n={n} ({registro['regimen']}), predicciones: {preds}")
    print(f"escrito {destino.relative_to(ROOT).as_posix()}: haz commit ANTES de leer el C oficial.")


def cmd_verificar(args: argparse.Namespace) -> None:
    path = Path(args.archivo)
    registro = json.loads(path.read_text(encoding="utf-8"))
    if registro.get("resultado"):
        sys.exit("esta predicción ya tiene resultado")
    largo = registro["n"] >= N_FRONTERA
    aciertos = {k: acierta(v, args.C, largo) for k, v in registro["predicciones"].items()}
    registro["resultado"] = {
        "C_oficial": args.C,
        "verificado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "aciertos": aciertos,
        "nota": args.nota or "",
    }
    path.write_text(json.dumps(registro, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, ok in aciertos.items():
        print(f"{k:<22} pred={registro['predicciones'][k]:<10} {'ACIERTO' if ok else 'fallo'}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("evaluar")
    p.add_argument("--reglas")
    p.add_argument("--conjuntos", default="maestro,2m,nuevos", help="maestro, 2m o ambos separados por coma")
    p.add_argument("--json")
    p.set_defaults(func=cmd_evaluar)
    p = sub.add_parser("registrar")
    p.add_argument("--ohlcv", required=True)
    p.add_argument("--start", required=True)
    p.add_argument("--end", required=True)
    p.add_argument("--dt", required=True, type=int)
    p.add_argument("--simbolo", default="CME_MINI:NQ1!")
    p.add_argument("--reglas")
    p.add_argument("--nota")
    p.set_defaults(func=cmd_registrar)
    p = sub.add_parser("verificar")
    p.add_argument("--archivo", required=True)
    p.add_argument("--C", required=True, type=float)
    p.add_argument("--nota")
    p.set_defaults(func=cmd_verificar)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
