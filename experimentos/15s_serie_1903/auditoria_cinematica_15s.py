#!/usr/bin/env python3
"""
Auditoría cinemática de la serie EXP-20261014-1903-15S.
Evalúa la hipótesis de Luna / FrankyProfit:
Retención del impulso al cierre intraminuto (mecha superior, posición de cierre y monotonía).
"""
from pathlib import Path
import csv
from datetime import datetime, timezone
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CSV_BARS = ROOT / "C_barrido_15s_start1902.csv"

with CSV_BARS.open("r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

t_start = int(datetime(2026, 10, 12, 19, 3, 0, tzinfo=timezone.utc).timestamp())
t_end_max = int(datetime(2026, 10, 12, 19, 36, 0, tzinfo=timezone.utc).timestamp())

bars_1m = {}
for t in range(t_start, t_end_max + 60, 60):
    sub = [bars_15s[t + s] for s in [0, 15, 30, 45]]
    bars_1m[t] = {
        "time": t,
        "dt": datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"),
        "open": float(sub[0]["open"]),
        "high": max(float(b["high"]) for b in sub),
        "low": min(float(b["low"]) for b in sub),
        "close": float(sub[3]["close"]),
        "subbars": sub
    }

observed_15s = {
    "19:23": 88, "19:24": 67, "19:25": 88, "19:26": 88, "19:27": 79,
    "19:28": 102, "19:29": 123, "19:30": 67, "19:31": 87, "19:32": 106,
    "19:33": 87, "19:34": 123, "19:35": 87
}

print(f"{'n':>2} | {'END':>5} | {'C_15s':>5} | {'Rng':>5} | {'Cuerpo':>6} | {'MechaSup':>8} | {'Pos%':>6} | {'MaxSub':>6} | {'Monotona':>8} | {'Clasificación':<15}")
print("-" * 80)

win_h = -1e9
for m in range(23, 36):
    n = m - 2
    dt_str = f"19:{m:02d}"
    t = int(datetime(2026, 10, 12, 19, m, 0, tzinfo=timezone.utc).timestamp())
    b = bars_1m[t]
    
    rng = b["high"] - b["low"]
    body = b["close"] - b["open"]
    uwick = b["high"] - max(b["open"], b["close"])
    pos_pct = (b["close"] - b["low"]) / rng * 100.0 if rng > 0 else 50.0
    
    sub = b["subbars"]
    sub_c = [float(sb["close"]) for sb in sub]
    sub_h = [float(sb["high"]) for sb in sub]
    
    max_idx = int(np.argmax(sub_h))
    sub_names = [":00", ":15", ":30", ":45"]
    max_sub = sub_names[max_idx]
    
    monotonic = all(sub_c[i] < sub_c[i+1] for i in range(3))
    c_val = observed_15s[dt_str]
    
    if c_val >= 120:
        clasif = "PICO MAYOR"
    elif c_val >= 100:
        clasif = "IMPULSO MEDIO"
    elif c_val == 87:
        clasif = "MESETA BASE"
    else:
        clasif = "VALLE / RETRACC."
        
    print(f"{n:>2} | {dt_str:>5} | {c_val:>5} | {rng:>5.2f} | {body:>+6.2f} | {uwick:>8.2f} | {pos_pct:>5.1f}% | {max_sub:>6} | {str(monotonic):>8} | {clasif}")
