import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

# Load training cases
train_cases = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Loaded {len(train_cases)} training cases.")

# For each case, compute basic accumulator variables that a Pine Script loop would compute:
rows = []
for c in train_cases:
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    opens = np.array([b["open"] for b in ohlc])
    highs = np.array([b["high"] for b in ohlc])
    lows = np.array([b["low"] for b in ohlc])
    closes = np.array([b["close"] for b in ohlc])
    times = np.array([b["time"] for b in ohlc])
    
    # 1. Price extremes and their bar indices
    idx_hi = int(np.argmax(highs))
    idx_lo = int(np.argmin(lows))
    max_hi = highs[idx_hi]
    min_lo = lows[idx_lo]
    
    # 2. First candle and last candle
    first_o = opens[0]
    first_h = highs[0]
    first_l = lows[0]
    first_c = closes[0]
    last_c = closes[-1]
    last_h = highs[-1]
    last_l = lows[-1]
    
    # 3. Time distance between extremes
    # Distances in bars
    dist_hi_lo = abs(idx_hi - idx_lo)
    dist_start_lo = idx_lo
    dist_start_hi = idx_hi
    dist_lo_end = n - 1 - idx_lo
    dist_hi_end = n - 1 - idx_hi
    
    # 4. Range amplitude
    rng = max_hi - min_lo
    
    # 5. Sum of true range, ATR
    tr = np.maximum(highs - lows, np.abs(highs - np.roll(closes, 1)))
    tr[0] = highs[0] - lows[0]
    sum_tr = np.sum(tr)
    
    # 6. Sum of candle ranges
    sum_hl = np.sum(highs - lows)
    
    # 7. Close-to-open net change
    net_change = abs(last_c - first_o)
    
    rows.append({
        "id": c["id"],
        "n": n,
        "dt": dt,
        "C": int(round(c["C"])),
        "idx_hi": idx_hi,
        "idx_lo": idx_lo,
        "dist_hi_lo": dist_hi_lo,
        "dist_start_lo": dist_start_lo,
        "dist_start_hi": dist_start_hi,
        "dist_lo_end": dist_lo_end,
        "dist_hi_end": dist_hi_end,
        "rng": rng,
        "sum_hl": sum_hl,
        "sum_tr": sum_tr,
        "net_change": net_change,
        "first_c": first_c,
        "last_c": last_c
    })

# Check correlations with C (or C/dt)
import pandas as pd
df = pd.DataFrame(rows)
print("Data summary of training cases:")
print(df[["id", "n", "dt", "C", "idx_hi", "idx_lo", "dist_hi_lo", "rng"]].to_string())
