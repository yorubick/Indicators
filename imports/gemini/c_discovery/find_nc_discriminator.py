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
        "volume": sum(float(b.get("volume", 0)) for b in sub), # if available
        "subbars": sub
    })

time_to_idx = {b["dt"]: i for i, b in enumerate(bars_1m)}

# Cases 19:28 to 19:35 where NC is either 5 or 6 (or 4)
# 19:28: C=88  (NC=4)
# 19:29: C=135 (NC=6)
# 19:30: C=112 (NC=5)
# 19:31: C=136 (NC=6)
# 19:32: C=112 (NC=5)
# 19:33: C=112 (NC=5)
# 19:34: C=135 (NC=6)
# 19:35: C=112 (NC=5)

target_nc = {
    "19:28": 4,
    "19:29": 6,
    "19:30": 5,
    "19:31": 6,
    "19:32": 5,
    "19:33": 5,
    "19:34": 6,
    "19:35": 5,
}

print("=== TESTING EXACT DISCRIMINATOR FOR NC (5 vs 6) ===")
# Let's inspect all candle properties of each of these 8 candles
for dt_str, nc in target_nc.items():
    idx = time_to_idx[dt_str]
    b = bars_1m[idx]
    prev = bars_1m[idx-1]
    prev2 = bars_1m[idx-2]
    
    rng = b["high"] - b["low"]
    body = b["close"] - b["open"]
    uwick = b["high"] - max(b["open"], b["close"])
    lwick = min(b["open"], b["close"]) - b["low"]
    
    # Check swing / pivot features:
    # Is previous bar a pivot high? (high[1] > high[2] and high[1] > high[0])
    is_prev_pivot_h = prev["high"] > prev2["high"] and prev["high"] > b["high"]
    
    # Distance to previous high
    dist_prev_h = b["high"] - prev["high"]
    dist_prev_c = b["close"] - prev["close"]
    
    # Breakout of previous high
    brk_h = b["high"] > prev["high"]
    brk_c = b["close"] > prev["high"]
    
    # Range expansion: rng > prev rng
    rng_exp = rng > (prev["high"] - prev["low"])
    
    # Sub-bar dynamics
    sub = b["subbars"]
    sub_closes = [float(sb["close"]) for sb in sub]
    sub_highs = [float(sb["high"]) for sb in sub]
    sub_rngs = [float(sb["high"]) - float(sb["low"]) for sb in sub]
    
    # Last sub-bar is bullish and closes near high
    last_sub_uwick = sub_highs[3] - sub_closes[3]
    last_sub_body = sub_closes[3] - float(sub[3]["open"])
    
    print(f"{dt_str} | NC={nc} | Rng={rng:4.2f} | Body={body:+5.2f} | UW={uwick:4.2f} | brk_c={str(brk_c):<5} | rng_exp={str(rng_exp):<5} | sub_closes={[round(x, 1) for x in sub_closes]}")
