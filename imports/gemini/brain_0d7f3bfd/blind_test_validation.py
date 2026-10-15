import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

val_cases = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "validation"]
print(f"=== BLIND EVALUATION ON {len(val_cases)} RESERVED VALIDATION CASES ===\n")

def predict_c_frozen(ohlc, dt):
    n = len(ohlc)
    highs = np.array([b["high"] for b in ohlc])
    lows = np.array([b["low"] for b in ohlc])
    closes = np.array([b["close"] for b in ohlc])
    opens = np.array([b["open"] for b in ohlc])
    
    i_max = int(np.argmax(highs))
    i_min = int(np.argmin(lows))
    bs_max = n - 1 - i_max
    bs_min = n - 1 - i_min
    
    rng_tot = highs[i_max] - lows[i_min]
    rng_0 = highs[0] - lows[0]
    first_ext = min(i_max, i_min)
    
    # Check timeframe:
    if dt != 60:
        # Scale to dt:
        return round(n * dt * 10.0 / 183.0)
    
    # 1. Check for Active Breakout:
    # If the last bar is at or within 1 bar of the new high after an expansion:
    # In training, C was 71 when highs exceeded the channel high.
    # What is the relative expansion?
    
    # 2. Check for Consolidation State (M = 24):
    # Condition calibrated on training: first_ext >= 6 and rng_0 / rng_tot <= 0.35:
    is_interior_consolidation = (first_ext >= 6 and (rng_0 / rng_tot) <= 0.35)
    
    if is_interior_consolidation and bs_max > 0:
        return int(np.floor((n - 1) * dt / 24.0))
    
    # 3. Base State or Trend:
    # For general windows:
    return 77

# Let's inspect each validation case:
results = []
for c in val_cases:
    ohlc = c["OHLC"]
    n = c["bars"]
    dt = c["dt"]
    act_c = round(c["C"])
    pred_c = predict_c_frozen(ohlc, dt)
    st = c["START"][11:16]
    en = c["END"][11:16]
    diff = abs(act_c - pred_c)
    
    # Feature metrics
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    i_max = highs.index(max(highs))
    i_min = lows.index(min(lows))
    first_ext = min(i_max, i_min)
    rng_tot = max(highs) - min(lows)
    r0 = (highs[0] - lows[0]) / rng_tot if rng_tot else 0
    
    results.append({
        "id": c["id"][:28],
        "st_en": f"{st}-{en}",
        "n": n,
        "dt": dt,
        "act_c": act_c,
        "pred_c": pred_c,
        "diff": diff,
        "first_ext": first_ext,
        "i_max": i_max,
        "i_min": i_min,
        "r0": round(r0, 3),
        "rng": round(rng_tot, 2)
    })

import pandas as pd
df = pd.DataFrame(results)
print(df[["st_en", "n", "act_c", "pred_c", "diff", "first_ext", "i_max", "i_min", "r0", "rng"]].to_string())

exact_matches = sum(r["diff"] == 0 for r in results)
within_5 = sum(r["diff"] <= 5 for r in results)
print(f"\nExact matches: {exact_matches} / {len(val_cases)} ({exact_matches/len(val_cases)*100:.1f}%)")
print(f"Within 5s:     {within_5} / {len(val_cases)} ({within_5/len(val_cases)*100:.1f}%)")
print(f"Mean Absolute Error: {np.mean([r['diff'] for r in results]):.2f} seconds")
