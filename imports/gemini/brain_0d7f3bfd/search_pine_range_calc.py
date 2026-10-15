import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Loaded {len(train)} training cases.")

# Let's inspect: What simple mathematical operators on a range of bars exist in Pine Script?
# 1. Volume-weighted or range-weighted metrics? (No volume in dataset)
# 2. Distance from lowest low to highest high?
# 3. Time elapsed between extremes?
# 4. Standard deviation of price?
# 5. ATR of the range?
# 6. Number of swings or fractals?
# 7. Kaufman efficiency ratio or fractal dimension?

# Let's compute these for all 32 training cases:
table = []
for c in train:
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    highs = np.array([b["high"] for b in ohlc])
    lows = np.array([b["low"] for b in ohlc])
    closes = np.array([b["close"] for b in ohlc])
    opens = np.array([b["open"] for b in ohlc])
    
    # Highest and Lowest
    h_max = np.max(highs)
    l_min = np.min(lows)
    i_max = int(np.argmax(highs))
    i_min = int(np.argmin(lows))
    
    # Range
    rng = h_max - l_min
    
    # Standard deviation of close
    std_c = np.std(closes)
    
    # Mean True Range
    tr = np.maximum(highs - lows, np.abs(highs - np.roll(closes, 1)))
    tr[0] = highs[0] - lows[0]
    atr = np.mean(tr)
    
    # Swing points: fractal 2-bar left and right
    # (high[2] > high[1] and high[2] > high[0] and high[2] > high[3] and high[2] > high[4])
    piv_h2 = [i for i in range(2, n - 2) if highs[i] == max(highs[i-2:i+3])]
    piv_l2 = [i for i in range(2, n - 2) if lows[i] == min(lows[i-2:i+3])]
    total_fractals = len(piv_h2) + len(piv_l2)
    
    # Distance between global extremes in seconds
    t_hl = abs(i_max - i_min) * dt
    
    # Total span in seconds
    t_span = (n - 1) * dt
    
    c_target = int(round(c["C"]))
    
    table.append({
        "id": c["id"][:26],
        "n": n,
        "dt": dt,
        "C": c_target,
        "rng": rng,
        "std_c": round(std_c, 2),
        "atr": round(atr, 2),
        "fractals": total_fractals,
        "t_hl": t_hl,
        "t_span": t_span,
        "C_over_span": round(c_target / t_span, 4) if t_span else 0
    })

import pandas as pd
df = pd.DataFrame(table)
print(df.to_string())
