#!/usr/bin/env python3
"""
Reproducción e inversión exacta de C para la serie EXP-20261014-1903-15S.
Carga barras de 15s desde G:/trading/guias/analisis/C_barrido_15s_start1902.csv
e invierte C para cada una de las 13 mediciones oficiales registradas.
"""
from pathlib import Path
import csv
import json
from datetime import datetime, timezone
from scipy.optimize import brentq
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CSV_BARS = ROOT / "C_barrido_15s_start1902.csv"

# Cargar barras de 15s
with CSV_BARS.open("r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Lecturas oficiales primarias de la Ventana de Datos en TradingView
cases = [
    {"n": 21, "END": "19:23", "eval": "19:26", "readings": {"Lane 3 A": 30864.97, "Lane 3 B": 30864.84, "Lane 2 A": 30866.12, "Lane 2 B": 30865.82, "Lane 1 A": 30868.16, "Lane 1 B": 30867.73}},
    {"n": 22, "END": "19:24", "eval": "19:26", "readings": {"Lane 3 A": 30866.67, "Lane 3 B": 30866.59, "Lane 2 A": 30867.37, "Lane 2 B": 30867.18, "Lane 1 A": 30868.74, "Lane 1 B": 30868.43}},
    {"n": 23, "END": "19:25", "eval": "19:26", "readings": {"Lane 3 A": 30867.16, "Lane 3 B": 30867.13, "Lane 2 A": 30867.46, "Lane 2 B": 30867.38, "Lane 1 A": 30868.23, "Lane 1 B": 30868.03}},
    {"n": 24, "END": "19:26", "eval": "19:30", "readings": {"Lane 3 A": 30868.47, "Lane 3 B": 30868.26, "Lane 2 A": 30870.30, "Lane 2 B": 30869.85, "Lane 1 A": 30873.03, "Lane 1 B": 30872.50}},
    {"n": 25, "END": "19:27", "eval": "19:30", "readings": {"Lane 3 A": 30871.42, "Lane 3 B": 30871.35, "Lane 2 A": 30872.13, "Lane 2 B": 30871.94, "Lane 1 A": 30873.52, "Lane 1 B": 30873.21}},
    {"n": 26, "END": "19:28", "eval": "19:30", "readings": {"Lane 3 A": 30869.92, "Lane 3 B": 30869.84, "Lane 2 A": 30870.67, "Lane 2 B": 30870.47, "Lane 1 A": 30872.35, "Lane 1 B": 30871.94}},
    {"n": 27, "END": "19:29", "eval": "19:30", "readings": {"Lane 3 A": 30870.68, "Lane 3 B": 30870.65, "Lane 2 A": 30871.03, "Lane 2 B": 30870.93, "Lane 1 A": 30871.94, "Lane 1 B": 30871.69}},
    {"n": 28, "END": "19:30", "eval": "19:32", "readings": {"Lane 3 A": 30871.78, "Lane 3 B": 30871.64, "Lane 2 A": 30873.09, "Lane 2 B": 30872.75, "Lane 1 A": 30875.60, "Lane 1 B": 30875.04}},
    {"n": 29, "END": "19:31", "eval": "19:32", "readings": {"Lane 3 A": 30872.59, "Lane 3 B": 30872.53, "Lane 2 A": 30873.22, "Lane 2 B": 30873.04, "Lane 1 A": 30874.76, "Lane 1 B": 30874.37}},
    {"n": 30, "END": "19:32", "eval": "19:33", "readings": {"Lane 3 A": 30874.84, "Lane 3 B": 30874.77, "Lane 2 A": 30875.47, "Lane 2 B": 30875.29, "Lane 1 A": 30877.10, "Lane 1 B": 30876.67}},
    {"n": 31, "END": "19:33", "eval": "19:34", "readings": {"Lane 3 A": 30877.88, "Lane 3 B": 30877.71, "Lane 2 A": 30879.51, "Lane 2 B": 30879.06, "Lane 1 A": 30883.53, "Lane 1 B": 30882.49}},
    {"n": 32, "END": "19:34", "eval": "19:35", "readings": {"Lane 3 A": 30886.45, "Lane 3 B": 30886.32, "Lane 2 A": 30887.77, "Lane 2 B": 30887.40, "Lane 1 A": 30891.16, "Lane 1 B": 30890.27}},
    {"n": 33, "END": "19:35", "eval": "19:36", "readings": {"Lane 3 A": 30896.10, "Lane 3 B": 30895.99, "Lane 2 A": 30897.22, "Lane 2 B": 30896.91, "Lane 1 A": 30899.97, "Lane 1 B": 30899.26}},
]

factors = {
    "Lane 3 A": 24.0,           # Lane A Fast
    "Lane 3 B": 89.0 / 3.0,     # Lane A Slow
    "Lane 2 A": 8.0,            # Lane B Fast
    "Lane 2 B": 89.0 / 9.0,     # Lane B Slow
    "Lane 1 A": 72.0 / 27.0,    # Lane C Fast
    "Lane 1 B": 89.0 / 27.0,    # Lane C Slow
}

dt = 15.0

print(f"{'n':>2} | {'END':>5} | {'C_int':>5} | {'Media_6':>7} | {'Spread':>6} | {'Max_Residuo (pts)':>18} | {'Estado':<10}")
print("-" * 65)

for c in cases:
    n = c["n"]
    end_str = c["END"]
    eval_str = c["eval"]
    readings = c["readings"]
    
    h, m = map(int, end_str.split(":"))
    t_end_00 = int(datetime(2026, 10, 12, h, m, 0, tzinfo=timezone.utc).timestamp())
    t_end_45 = t_end_00 + 45
    
    eh, em = map(int, eval_str.split(":"))
    t_eval_45 = int(datetime(2026, 10, 12, eh, em, 45, tzinfo=timezone.utc).timestamp())
    
    seed = min(float(bars_15s[t]["low"]) for t in range(t_end_00, t_end_45 + 1, 15))
    closes = [float(bars_15s[t]["close"]) for t in range(t_end_45 + 15, t_eval_45 + 1, 15)]
    
    solved = {}
    for lane, obs in readings.items():
        b0 = factors[lane]
        def sim(c_val):
            alpha = 2.0 / ((b0 * c_val / dt) + 1.0)
            st = seed
            for cl in closes:
                st += alpha * (cl - st)
            return st
        try:
            sol = brentq(lambda c_v: sim(c_v) - obs, 5.0, 1500.0)
            solved[lane] = sol
        except:
            solved[lane] = None
            
    valid = [v for v in solved.values() if v is not None]
    avg_c = np.mean(valid)
    int_c = round(avg_c)
    spread = max(valid) - min(valid)
    
    # Calcular residuo máximo del entero frente a las 6 lecturas oficiales
    max_err = 0.0
    for lane, obs in readings.items():
        b0 = factors[lane]
        alpha = 2.0 / ((b0 * int_c / dt) + 1.0)
        st = seed
        for cl in closes:
            st += alpha * (cl - st)
        err = abs(st - obs)
        if err > max_err:
            max_err = err
            
    estado = "PASA (<0.005)" if max_err < 0.005 else "FALLA"
    print(f"{n:>2} | {end_str:>5} | {int_c:>5} | {avg_c:>7.2f} | {spread:>6.2f} | {max_err:>18.4f} | {estado}")
