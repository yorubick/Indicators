import csv
import json
import pandas as pd
import numpy as np

# Cargar las mediciones de 15s
with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Casos observados en la serie 19:03
cases_15s = [
    ("19:23", 88),
    ("19:24", 67),
    ("19:25", 88),
    ("19:26", 88),
    ("19:27", 79),
    ("19:28", 102),
    ("19:29", 123),
    ("19:30", 67),
    ("19:31", 87),
    ("19:32", 106),
    ("19:33", 87),
    ("19:34", 123),
    ("19:35", 87),
]

t_start = 1791831780 # 19:03:00 UTC

print("=== ANÁLISIS DE LA CINEMÁTICA Y ACCIÓN DEL PRECIO EN CADA ESCALÓN (15s) ===")
print(f"{'END':<6} | {'C':<4} | {'Close':<9} | {'High':<9} | {'Low':<9} | {'Rng1m':<6} | {'Body1m':<7} | {'Diff_Prev_C':<11} | {'Comportamiento Mercado'}")
print("-" * 95)

prev_c = None
for end_str, c_val in cases_15s:
    eh, em = map(int, end_str.split(":"))
    # Timestamp del minuto END
    # 12-oct-2026
    # 19:03:00 es 1791831780 -> 19:23:00 es 1791831780 + 20*60 = 1791832980
    t_end_m = t_start + (int(end_str.split(":")[1]) - 3) * 60
    
    # 4 velas de 15s del minuto END
    sub_t = [t_end_m, t_end_m + 15, t_end_m + 30, t_end_m + 45]
    sub_bars = [bars_15s[t] for t in sub_t if t in bars_15s]
    
    o_1m = float(sub_bars[0]["open"])
    c_1m = float(sub_bars[-1]["close"])
    h_1m = max(float(b["high"]) for b in sub_bars)
    l_1m = min(float(b["low"]) for b in sub_bars)
    rng_1m = h_1m - l_1m
    body_1m = c_1m - o_1m
    
    diff_prev = f"{c_val - prev_c:+3d}" if prev_c is not None else "  0"
    prev_c = c_val
    
    # Descripción
    desc = ""
    if c_val == 123:
        desc = "Ruptura alcista violenta / Nuevo High"
    elif c_val == 67:
        desc = "Vela bajista / Retroceso profundo"
    elif c_val == 87 or c_val == 88:
        desc = "Consolidación / Vela neutral"
    elif c_val == 106 or c_val == 102:
        desc = "Impulso previo / Continuación"
    elif c_val == 79:
        desc = "Contracción menor"
        
    print(f"{end_str:<6} | {c_val:<4} | {c_1m:<9.2f} | {h_1m:<9.2f} | {l_1m:<9.2f} | {rng_1m:<6.2f} | {body_1m:<+7.2f} | {diff_prev:<11} | {desc}")
