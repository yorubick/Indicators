"""Recupera C de una exportación de Lite cuando la fuente es más fina que el gráfico.

Simula las seis EMA del Lite con las velas reales de la fuente (p. ej. 15 s),
sembradas en el extremo de la vela END del gráfico, y busca el C que reproduce
los valores exportados en cada vela del gráfico (valor tras la última subvela).
Prueba semilla en el máximo y en el mínimo de END y se queda con el menor residuo.

Uso:
  python tools/invertir_C_subfuente.py CSV FUENTE.json --end 2026-10-16T17:00 --dt 15 [--grafico 60] [--velas 20]
FUENTE.json: salida del conector de TradingView (bars con t/o/h/l/c/v).
"""
import argparse, csv, json, datetime as dt
from pathlib import Path

B0 = {"Lane 3 A": 24.0, "Lane 3 B": 89 / 3, "Lane 2 A": 8.0, "Lane 2 B": 89 / 9, "Lane 1 A": 8 / 3, "Lane 1 B": 89 / 27}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", type=Path); ap.add_argument("fuente", type=Path)
    ap.add_argument("--end", required=True); ap.add_argument("--dt", type=float, required=True)
    ap.add_argument("--grafico", type=int, default=60); ap.add_argument("--velas", type=int, default=20)
    a = ap.parse_args()
    end = int(dt.datetime.fromisoformat(a.end + ":00+00:00").timestamp())
    filas = {int(float(r["time"])): r for r in csv.DictReader(a.csv.open(encoding="utf-8-sig"))}
    b = json.loads(a.fuente.read_text())["bars"]
    sub = [(t, c) for t, c in zip(b["t"], b["c"]) if t >= end + a.grafico]
    g_end = filas[end]
    objetivos = [t for t in sorted(filas) if t > end and filas[t]["Lane 1 A"]][: a.velas]

    def simular(C, b0, seed):
        alpha = 2 / (b0 * C / a.dt + 1)
        L, out, i = seed, {}, 0
        for t in objetivos:
            while i < len(sub) and sub[i][0] < t + a.grafico:
                L += alpha * (sub[i][1] - L); i += 1
            out[t] = L
        return out

    mejor = None
    for nombre_seed in ("high", "low"):
        seed = float(g_end[nombre_seed])
        Cs, res = [], 0.0
        for carril, b0 in B0.items():
            reales = {t: float(filas[t][carril]) for t in objetivos}
            err = lambda C: sum((simular(C, b0, seed)[t] - reales[t]) ** 2 for t in objetivos)
            lo, hi = 1.0, 3000.0
            for _ in range(200):           # búsqueda por sección dorada
                m1, m2 = lo + (hi - lo) * 0.382, lo + (hi - lo) * 0.618
                if err(m1) < err(m2): hi = m2
                else: lo = m1
            C = (lo + hi) / 2
            Cs.append(C); res = max(res, max(abs(simular(C, b0, seed)[t] - reales[t]) for t in objetivos))
        cand = (res, nombre_seed, Cs)
        if mejor is None or cand[0] < mejor[0]: mejor = cand
    res, seed, Cs = mejor
    print(f"{a.csv.name}: semilla END {seed}; C por carril = {[round(c, 4) for c in Cs]}; residuo máximo {res:.6f} pt en {len(objetivos)} velas")


if __name__ == "__main__":
    main()
