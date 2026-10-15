import csv
from datetime import datetime, timezone
import numpy as np

# Load 15s bars from C_barrido_15s_start1902.csv
with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Build 1m bars from 18:50 to 19:40
t_start_build = int(datetime(2026, 10, 12, 18, 50, 0, tzinfo=timezone.utc).timestamp())
t_end_build = int(datetime(2026, 10, 12, 19, 40, 0, tzinfo=timezone.utc).timestamp())

bars_1m = []
for t in range(t_start_build, t_end_build + 60, 60):
    sub = [bars_15s[t + s] for s in [0, 15, 30, 45]]
    bars_1m.append({
        "time": t,
        "dt": datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"),
        "open": float(sub[0]["open"]),
        "high": max(float(b["high"]) for b in sub),
        "low": min(float(b["low"]) for b in sub),
        "close": float(sub[3]["close"]),
        "subbars": sub
    })

time_to_idx = {b["dt"]: i for i, b in enumerate(bars_1m)}

# Target C for 1m (19:26 to 19:35)
targets = {
    "19:26": 135,
    "19:27": 130,
    "19:28": 88,
    "19:29": 135,
    "19:30": 112,
    "19:31": 136,
    "19:32": 112,
    "19:33": 112,
    "19:34": 135,
    "19:35": 112,
}

# Let's inspect the exact formula candidates
# Candidate Equation:
# C = C_base + delta_C * E(t)
# where C_base = 112, delta_C = 23 (or 24)
# What is E(t)?
# E(t) in {19:26, 19:27, 19:29, 19:31, 19:34} is 1
# E(t) in {19:28, 19:30, 19:32, 19:33, 19:35} is 0 (with 19:28 being -1 -> 88)

print("=== SEARCHING FOR EXACT DETERMINISTIC FORMULA FOR E(t) ===")

# Test features:
# Let's look at the relation between the current bar high/close and the recent swings
for dt, c_val in targets.items():
    idx = time_to_idx[dt]
    b = bars_1m[idx]
    prev = bars_1m[idx-1]
    
    # 1. Breakout above high[1]
    # 2. Breakout above high[2]
    # 3. New high of session AND ...
    h = b["high"]
    l = b["low"]
    c = b["close"]
    rng = h - l
    
    # Intraday momentum of the 1m candle:
    # Look at subbars
    sub = b["subbars"]
    sub_closes = [float(sb["close"]) for sb in sub]
    sub_highs = [float(sb["high"]) for sb in sub]
    
    # Feature A: Did the candle make a new high AND close above the midpoint of the last 3 candles?
    # Feature B: Distance from close to high
    uwick = h - c
    
    # Feature C: Look at the 15s structure inside the minute
    # In 19:26: closes = [30868.5, 30869.5, 30869.0, 30872.5] -> last close is HIGHEST of minute
    # In 19:29: closes = [30871.8, 30871.8, 30872.2, 30875.8] -> last close is HIGHEST of minute
    # In 19:31: closes = [30877.2, 30874.5, 30873.2, 30874.5] -> peak was at :00, then pulled back
    # In 19:34: closes = [30888.8, 30891.0, 30893.8, 30897.2] -> last close is HIGHEST of minute
    
    last_is_highest = (sub_closes[3] == max(sub_closes))
    
    print(f"{dt} | C={c_val:>3} | h={h:8.2f} | c={c:8.2f} | uwick={uwick:4.2f} | last_is_highest={str(last_is_highest):<5}")
