import csv
from datetime import datetime, timezone
import json

with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Build 1m bars from 15s bars from 19:03 to 19:36
bars_1m = []
t_start = int(datetime(2026, 10, 12, 19, 3, 0, tzinfo=timezone.utc).timestamp())
t_end_max = int(datetime(2026, 10, 12, 19, 36, 45, tzinfo=timezone.utc).timestamp())

for m in range(3, 37):
    t0 = int(datetime(2026, 10, 12, 19, m, 0, tzinfo=timezone.utc).timestamp())
    sub = [bars_15s[t0 + i*15] for i in range(4) if (t0 + i*15) in bars_15s]
    if len(sub) == 4:
        bars_1m.append({
            "minute": f"19:{m:02d}",
            "time": t0,
            "open": float(sub[0]["open"]),
            "high": max(float(b["high"]) for b in sub),
            "low": min(float(b["low"]) for b in sub),
            "close": float(sub[3]["close"]),
            "subbars": sub
        })

print(f"Loaded {len(bars_1m)} 1m bars from 19:03 to 19:36.")

# Known C values for END 19:23 to 19:35 (with START 19:03)
known_C = {
    "19:23": {"C_15s": 88, "C_1m": 50},
    "19:24": {"C_15s": 67, "C_1m": 52},
    "19:25": {"C_15s": 88, "C_1m": 71},
    "19:26": {"C_15s": 88, "C_1m": 135},
    "19:27": {"C_15s": 79, "C_1m": 130},
    "19:28": {"C_15s": 102, "C_1m": 88},
    "19:29": {"C_15s": 123, "C_1m": 135},
    "19:30": {"C_15s": 67, "C_1m": 112},
    "19:31": {"C_15s": 87, "C_1m": 112},
    "19:32": {"C_15s": 106, "C_1m": 112},
    "19:33": {"C_15s": 87, "C_1m": 112},
    "19:34": {"C_15s": 123, "C_1m": 136},
    "19:35": {"C_15s": 87, "C_1m": 112},
}

# 1. Classical Swing Pivot detection (causal, radius L/R)
# A high at bar i is confirmed at bar i + R if high[i] > high[i-j] and high[i] >= high[i+k]
def detect_pivots_1m(bars, R=1):
    high_pivots = []
    low_pivots = []
    for i in range(R, len(bars) - R):
        h = bars[i]["high"]
        l = bars[i]["low"]
        is_hp = all(bars[i-j]["high"] < h for j in range(1, R+1)) and all(bars[i+k]["high"] <= h for k in range(1, R+1))
        is_lp = all(bars[i-j]["low"] > l for j in range(1, R+1)) and all(bars[i+k]["low"] >= l for k in range(1, R+1))
        if is_hp:
            high_pivots.append((i, bars[i]["minute"], h))
        if is_lp:
            low_pivots.append((i, bars[i]["minute"], l))
    return high_pivots, low_pivots

hp1, lp1 = detect_pivots_1m(bars_1m, R=1)
print("\n--- 1m Swing Highs (R=1) ---")
for p in hp1: print(f"  Bar {p[0]:2d} ({p[1]}): {p[2]:.2f}")
print("\n--- 1m Swing Lows (R=1) ---")
for p in lp1: print(f"  Bar {p[0]:2d} ({p[1]}): {p[2]:.2f}")
