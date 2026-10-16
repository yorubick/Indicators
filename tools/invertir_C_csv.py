"""Recupera C vela a vela a partir de una exportación CSV de PoiSzn EMA Origin Lite.

Para cada vela con curvas publicadas y cada carril, invierte la recurrencia EMA
    L_k = L_{k-1} + alpha (close_k - L_{k-1}),  alpha = 2 / (b0 * C / dt + 1)
con alpha = (L_k - L_{k-1}) / (close_k - L_{k-1}). Descarta pasos mal
condicionados (|close - L_{k-1}| < --min-dif) e informa de la mediana de los
seis carriles y de su dispersión. Si C cambia a lo largo de la serie, lo indica.

Requiere que el gráfico tenga la misma resolución que la fuente (una
actualización de la EMA por vela del CSV).

Uso:  python tools/invertir_C_csv.py manual/archivo_b.csv [--dt 60] [--detalle]
"""
from __future__ import annotations

import argparse
import csv
import statistics
from pathlib import Path

B0 = {"Lane 3 A": 24.0, "Lane 3 B": 89 / 3, "Lane 2 A": 8.0,
      "Lane 2 B": 89 / 9, "Lane 1 A": 8 / 3, "Lane 1 B": 89 / 27}


def invertir(path: Path, dt: float, min_dif: float) -> list[tuple[int, float, float, int]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        filas = list(csv.DictReader(handle))
    faltan = [c for c in ("time", "close", *B0) if c not in filas[0]]
    if faltan:
        raise SystemExit(f"{path}: faltan columnas {faltan}")
    salida, previa = [], None
    for fila in filas:
        if fila["Lane 1 A"] == "":
            previa = None
            continue
        if previa is not None:
            estimaciones = []
            for carril, b0 in B0.items():
                l0, l1, x = float(previa[carril]), float(fila[carril]), float(fila["close"])
                if abs(x - l0) < min_dif:
                    continue
                alpha = (l1 - l0) / (x - l0)
                if 0 < alpha < 1:
                    estimaciones.append((2 / alpha - 1) * dt / b0)
            if estimaciones:
                salida.append((int(float(fila["time"])), statistics.median(estimaciones),
                               max(estimaciones) - min(estimaciones), len(estimaciones)))
        previa = fila
    return salida


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("csv", nargs="+", type=Path)
    parser.add_argument("--dt", type=float, default=60.0, help="segundos por vela del CSV (= fuente)")
    parser.add_argument("--min-dif", type=float, default=0.5, help="puntos mínimos entre close y curva")
    parser.add_argument("--detalle", action="store_true")
    args = parser.parse_args()
    for path in args.csv:
        serie = invertir(path, args.dt, args.min_dif)
        buenas = [(t, c) for t, c, disp, k in serie if disp < 1.0 and k >= 4]
        if not buenas:
            print(f"{path}: sin velas con curvas utilizables")
            continue
        valores = [c for _, c in buenas]
        print(f"{path}: primera vela con curvas {serie[0][0]}, {len(buenas)} velas útiles; "
              f"C mediana = {statistics.median(valores):.4f} (mín {min(valores):.4f}, máx {max(valores):.4f})")
        anterior = None
        for t, c in buenas:
            if anterior is not None and abs(c - anterior) > 0.5:
                print(f"   C cambia en {t}: {anterior:.4f} -> {c:.4f}")
            anterior = c
        if args.detalle:
            for t, c, disp, k in serie[:15]:
                print(f"   {t} C={c:.5f} dispersión={disp:.5f} carriles={k}")


if __name__ == "__main__":
    main()
