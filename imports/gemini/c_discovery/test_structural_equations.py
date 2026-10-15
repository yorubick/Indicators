import csv
from datetime import datetime, timezone
import numpy as np

# Load 1m bars from master_all_C_cases
import json
with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

bars_1m = {}
for c in master["cases"]:
    if c.get("dt") == 60 and "2026-10-12" in c.get("START", ""):
        for b in c.get("OHLCV", []):
            bars_1m[b["time"]] = b

# Load 15s bars
with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Known C values
cases_info = [
    {"n": 21, "m": 23, "C_1m": 50, "C_15s": 88},
    {"n": 22, "m": 24, "C_1m": 52, "C_15s": 67},
    {"n": 23, "m": 25, "C_1m": 71, "C_15s": 88},
    {"n": 24, "m": 26, "C_1m": 135, "C_15s": 88},
    {"n": 25, "m": 27, "C_1m": 130, "C_15s": 79},
    {"n": 26, "m": 28, "C_1m": 88, "C_15s": 102},
    {"n": 27, "m": 29, "C_1m": 135, "C_15s": 123},
    {"n": 28, "m": 30, "C_1m": 112, "C_15s": 67},
    {"n": 29, "m": 31, "C_1m": 136, "C_15s": 87},
    {"n": 30, "m": 32, "C_1m": 112, "C_15s": 106},
    {"n": 31, "m": 33, "C_1m": 112, "C_15s": 87},
    {"n": 32, "m": 34, "C_1m": 135, "C_15s": 123},
    {"n": 33, "m": 35, "C_1m": 112, "C_15s": 87},
]

t_start = int(datetime(2026, 10, 12, 19, 3, 0, tzinfo=timezone.utc).timestamp())

print("=== CANDIDATE STRUCTURAL QUANTITIES (START 19:03 to END) ===")
print(f"{'m':>2} | {'C_1m':>5} | {'C_15s':>5} | {'Win_H':>8} | {'Win_L':>8} | {'Win_Rng':>7} | {'Bar_H':>8} | {'Bar_L':>8} | {'Bar_C':>8} | {'New_H?':>6} | {'BarsSinceLow':>12} | {'BarsSinceHigh':>13}")
print("-" * 115)

# Calculate running window metrics for 1m bars
running_high = -1e9
running_low = 1e9
high_bar_idx = 0
low_bar_idx = 0

all_1m_times = sorted([t for t in bars_1m.keys() if t >= t_start])

for idx, t in enumerate(all_1m_times):
    b = bars_1m[t]
    h = float(b["high"])
    l = float(b["low"])
    c = float(b["close"])
    
    is_new_h = h > running_high
    if h > running_high:
        running_high = h
        high_bar_idx = idx
    if l < running_low:
        running_low = l
        low_bar_idx = idx
        
    m_val = int(datetime.fromtimestamp(t, tz=timezone.utc).strftime("%M"))
    match = [ci for ci in cases_info if ci["m"] == m_val]
    if match:
        ci = match[0]
        bars_since_l = idx - low_bar_idx
        bars_since_h = idx - high_bar_idx
        win_rng = running_high - running_low
        print(f"{m_val:>2} | {ci['C_1m']:>5} | {ci['C_15s']:>5} | {running_high:>8.2f} | {running_low:>8.2f} | {win_rng:>7.2f} | {h:>8.2f} | {l:>8.2f} | {c:>8.2f} | {str(is_new_h):>6} | {bars_since_l:>12} | {bars_since_h:>13}")
