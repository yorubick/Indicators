import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Loaded {len(train)} training cases.")

# For each training case, let's test all possible pairs of timestamps (t_j - t_i) inside the range:
# Is C equal to round( (t_j - t_i) * K ) for some universal K?
# What if K is from the harmonic family:
# 10/183, 1/18, 1/15, 1/12, 1/10, 1/8, 1/6, 1/5, 1/4, 1/3, 2/3, 72/89, etc.?

candidate_Ks = [
    10/183, 20/183, 145/(61*60), 200/(61*60), 1/18, 1/16, 1/15, 1/14, 1/12, 1/10, 1/9, 1/8, 1/6, 1/5, 1/4, 1/3, 1/2,
    72/1800, 89/1800, 72/1200, 89/1200, 72/3600, 89/3600
]

# Let's inspect the ratio C / (t_j - t_i) for key structural points:
# Structural points:
# 0: START
# idx_min: Lowest Low
# idx_max: Highest High
# n-1: END

for i, c in enumerate(train[:10]):
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    c_val = round(c["C"])
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    i_max = highs.index(max(highs))
    i_min = lows.index(min(lows))
    
    t_span = (n - 1) * dt
    t_hl = abs(i_max - i_min) * dt
    t_min_end = (n - 1 - i_min) * dt
    t_max_end = (n - 1 - i_max) * dt
    t_start_min = i_min * dt
    t_start_max = i_max * dt
    
    print(f"[{i:2d}] n={n:2d} dt={dt:3d} C={c_val:3d} | span={t_span:4d} (r={c_val/t_span:.4f}) | t_hl={t_hl:4d} (r={c_val/t_hl if t_hl else 0:.4f}) | t_min_end={t_min_end:4d} | t_max_end={t_max_end:4d}")
