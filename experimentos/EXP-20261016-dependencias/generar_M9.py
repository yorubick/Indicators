"""M9 (17-oct): 30 ventanas independientes elegidas al azar (semilla fija) para
ampliar el número de bloques independientes del régimen largo.

Reglas del sorteo: fuente y gráfico 1 m, sesión ETH, días 12, 13, 15 y 16 de oct
(velas del conector ya guardadas), n entre 21 y 45 velas, sin cruzar el corte
diario (21:00-22:00 UTC) y sin solaparse con otra ventana del sorteo ni con
ventanas ya medidas. Las predicciones de las reglas existentes se escriben en
M9_ventanas.json antes de cualquier medición.
"""
import json, random, sys, datetime as dt
from pathlib import Path
AQUI = Path(__file__).parent
sys.path.insert(0, str(AQUI.parents[1] / "tools"))
from evaluador_C import (Caso, Vela, REGLAS_FIJAS, REGLAS_AJUSTABLES, cargar_maestro, cargar_2m,
                         cargar_nuevos, redondeo_pine)

random.seed(20261017)
barras = {}
for f in ("NQ1_1m_2026-10-12_13.json", "NQ1_1m_2026-10-15_16.json"):
    b = json.loads((AQUI / f).read_text())["bars"]
    for t, o, h, l, c, v in zip(b["t"], b["o"], b["h"], b["l"], b["c"], b["v"]):
        barras[t] = Vela(o, h, l, c, v)
ts = sorted(barras)

previas = [(r.ini, r.fin) for r in cargar_maestro() + cargar_2m() + cargar_nuevos()]
entreno = [r for r in cargar_maestro() + cargar_2m() + cargar_nuevos()]
reglas = {**REGLAS_FIJAS, **{k: f(entreno) for k, f in REGLAS_AJUSTABLES.items()}}

elegidas = []
intentos = 0
while len(elegidas) < 30 and intentos < 100000:
    intentos += 1
    ini = random.choice(ts)
    n = random.randint(21, 45)
    fin = ini + (n - 1) * 60
    d_ini = dt.datetime.fromtimestamp(ini, dt.timezone.utc)
    if d_ini.day not in (12, 13, 15, 16):
        continue
    if any(t not in barras for t in range(ini, fin + 1, 60)):
        continue                      # cruza el corte diario o faltan velas
    if any(not (fin < a - 300 or ini > b + 300) for a, b in previas + [(e["ini"], e["fin"]) for e in elegidas]):
        continue                      # solapa (margen de 5 min) con algo ya medido o sorteado
    velas = tuple(barras[t] for t in range(ini, fin + 1, 60))
    caso = Caso(60, n, fin - ini, velas)
    preds = {k: float(redondeo_pine(r(caso))) for k, r in reglas.items()}
    elegidas.append({"id": f"M9-{len(elegidas) + 1:02d}", "ini": ini, "fin": fin, "n": n,
                     "START": d_ini.strftime("%Y-%m-%d %H:%M"),
                     "END": dt.datetime.fromtimestamp(fin, dt.timezone.utc).strftime("%Y-%m-%d %H:%M"),
                     "archivo": f"M9_{d_ini:%m%d_%H%M}_{dt.datetime.fromtimestamp(fin, dt.timezone.utc):%H%M}.csv",
                     "predicciones": preds})
elegidas.sort(key=lambda e: e["ini"])
(AQUI / "M9_ventanas.json").write_text(json.dumps({"registrado": "2026-10-17", "semilla": 20261017, "ventanas": elegidas},
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
for e in elegidas:
    print(e["id"], e["START"], "→", e["END"][11:], "n =", e["n"], e["archivo"])
