import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Loaded {len(train)} training cases.")

# Let's test a state-tracking algorithm on each training case:
# State variables:
# - current_high
# - current_low
# - high_idx
# - low_idx
# - state: "CONSOLIDATION", "EXPANSION", "RETRACTED"

def run_state_machine(ohlc, dt):
    n = len(ohlc)
    # We iterate from bar 0 to n-1
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    closes = [b["close"] for b in ohlc]
    
    # We track extremes
    hi = highs[0]
    lo = lows[0]
    idx_hi = 0
    idx_lo = 0
    
    # Track breakout from first 5 bars (initial balance)
    ib_len = min(5, n)
    ib_high = max(highs[:ib_len])
    ib_low = min(lows[:ib_len])
    
    # State tracking
    is_expanding = False
    is_interior_peak = False
    
    # Last bar features
    i_max = int(np.argmax(highs))
    i_min = int(np.argmin(lows))
    
    bs_max = n - 1 - i_max
    bs_min = n - 1 - i_min
    
    # Range
    rng = max(highs) - min(lows)
    
    return {
        "n": n,
        "dt": dt,
        "rng": rng,
        "i_max": i_max,
        "i_min": i_min,
        "bs_max": bs_max,
        "bs_min": bs_min,
        "dist_hl": abs(i_max - i_min)
    }

results = []
for c in train:
    res = run_state_machine(c["OHLC"], c["dt"])
    res["C"] = int(round(c["C"]))
    res["id"] = c["id"]
    results.append(res)

import pandas as pd
df = pd.DataFrame(results)

# Group by (bs_max, bs_min) and see how C behaves
print("\nSummary by bs_max (bars since highest high):")
for bs, grp in df.groupby("bs_max"):
    print(f"bs_max = {bs:2d} ({len(grp):2d} cases): C values = {list(grp['C'].values)}")
