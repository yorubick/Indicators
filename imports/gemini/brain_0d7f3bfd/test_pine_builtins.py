import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Loaded {len(train)} training cases.")

# Let's inspect:
# 1. barssince highest high from END
# 2. barssince lowest low from END
# 3. barssince highest high from START
# 4. barssince lowest low from START
# 5. barssince breakout of initial balance (first bar, first 3 bars, first 5 bars)
# 6. barssince breakout of 50% equilibrium

rows = []
for c in train:
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    highs = np.array([b["high"] for b in ohlc])
    lows = np.array([b["low"] for b in ohlc])
    closes = np.array([b["close"] for b in ohlc])
    opens = np.array([b["open"] for b in ohlc])
    
    i_hi = int(np.argmax(highs))
    i_lo = int(np.argmin(lows))
    
    # Bars since highest high
    bs_hi = n - 1 - i_hi
    bs_lo = n - 1 - i_lo
    
    # 50% level
    mid = (np.max(highs) + np.min(lows)) / 2.0
    cross_mid = [i for i in range(n) if (closes[i] >= mid and opens[i] < mid) or (closes[i] <= mid and opens[i] > mid)]
    bs_cross_mid = n - 1 - cross_mid[-1] if cross_mid else n
    
    # First candle range
    ib_h = highs[0]
    ib_l = lows[0]
    first_break = [i for i in range(1, n) if closes[i] > ib_h or closes[i] < ib_l]
    ib_break_bar = first_break[0] if first_break else n
    
    # Last breakout
    h_roll = np.maximum.accumulate(highs)
    l_roll = np.minimum.accumulate(lows)
    
    c_target = int(round(c["C"]))
    
    rows.append({
        "id": c["id"][:28],
        "n": n,
        "dt": dt,
        "C": c_target,
        "bs_hi": bs_hi,
        "bs_lo": bs_lo,
        "i_hi": i_hi,
        "i_lo": i_lo,
        "ib_break": ib_break_bar,
        "dist_hi_lo": abs(i_hi - i_lo)
    })

import pandas as pd
df = pd.DataFrame(rows)
print(df.to_string())
