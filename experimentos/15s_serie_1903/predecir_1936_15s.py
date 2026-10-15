#!/usr/bin/env python3
"""
Predicción ciega a priori para END 19:36 UTC, evaluada en la vela 19:37 UTC.
Genera las curvas teóricas esperadas para contrastar en vivo en TradingView.
"""
from pathlib import Path
import csv
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
CSV_BARS = ROOT / "C_barrido_15s_start1902.csv"

with CSV_BARS.open("r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

t_end_00 = int(datetime(2026, 10, 12, 19, 36, 0, tzinfo=timezone.utc).timestamp())
t_end_45 = t_end_00 + 45
t_eval_45 = int(datetime(2026, 10, 12, 19, 37, 45, tzinfo=timezone.utc).timestamp())

# Semilla: Mínimo de la barra 19:36
seed = min(float(bars_15s[t]["low"]) for t in range(t_end_00, t_end_45 + 1, 15))

# Cierres de las 4 subbarras de 19:37
closes = [float(bars_15s[t]["close"]) for t in range(t_end_45 + 15, t_eval_45 + 1, 15)]

factors = {
    "Lane 3 A": 24.0,           # Lane A Fast
    "Lane 3 B": 89.0 / 3.0,     # Lane A Slow
    "Lane 2 A": 8.0,            # Lane B Fast
    "Lane 2 B": 89.0 / 9.0,     # Lane B Slow
    "Lane 1 A": 72.0 / 27.0,    # Lane C Fast
    "Lane 1 B": 89.0 / 27.0,    # Lane C Slow
}

dt = 15.0

print(f"Semilla END 19:36 (Low de 1m): {seed:.2f}")
print(f"Cierres subbarras 19:37: {closes}")
print("\n" + "=" * 65)
print("PREDICCIONES CIEGAS PARA EVALUACIÓN EN VELA 19:37 UTC")
print("=" * 65)

for c_cand in [87, 106, 123]:
    etiqueta = "PREDICCIÓN (Meseta)" if c_cand == 87 else "ALTERNATIVA"
    print(f"\n--- Si C_15s = {c_cand} ({etiqueta}) ---")
    for lane, b0 in factors.items():
        alpha = 2.0 / ((b0 * c_cand / dt) + 1.0)
        st = seed
        for cl in closes:
            st += alpha * (cl - st)
        print(f"  {lane:<9}: {st:.2f}")
