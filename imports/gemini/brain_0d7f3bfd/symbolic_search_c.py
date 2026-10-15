import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Loaded {len(train)} training cases.")

# Collect features for each training case
X = []
y = []
ids = []

for c in train:
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    opens = np.array([b["open"] for b in ohlc])
    highs = np.array([b["high"] for b in ohlc])
    lows = np.array([b["low"] for b in ohlc])
    closes = np.array([b["close"] for b in ohlc])
    times = np.array([b["time"] for b in ohlc])
    
    h_max = np.max(highs)
    l_min = np.min(lows)
    i_max = int(np.argmax(highs))
    i_min = int(np.argmin(lows))
    
    # 1. Price metrics
    rng = h_max - l_min
    body0 = closes[0] - opens[0]
    body_end = closes[-1] - opens[-1]
    net_c = closes[-1] - closes[0]
    
    # 2. Time metrics
    span_s = (n - 1) * dt
    bars_hi_lo = abs(i_max - i_min)
    time_hi_lo_s = bars_hi_lo * dt
    
    time_start_to_first_ext = min(i_max, i_min) * dt
    time_last_ext_to_end = (n - 1 - max(i_max, i_min)) * dt
    
    # 3. Sum of price changes
    hl_sum = np.sum(highs - lows)
    abs_dclose_sum = np.sum(np.abs(np.diff(closes)))
    
    # 4. First bar breakout time (how many bars until close or high leaves bar 0)
    b0_h = highs[0]
    b0_l = lows[0]
    break_h = [i for i in range(1, n) if highs[i] > b0_h]
    break_l = [i for i in range(1, n) if lows[i] < b0_l]
    first_break_bar = min(break_h[0] if break_h else n, break_l[0] if break_l else n)
    
    c_target = float(round(c["C"]))
    
    feat = {
        "n": n,
        "dt": dt,
        "rng": rng,
        "span_s": span_s,
        "bars_hi_lo": bars_hi_lo,
        "time_hi_lo_s": time_hi_lo_s,
        "time_start_first_ext": time_start_to_first_ext,
        "time_last_ext_end": time_last_ext_to_end,
        "hl_sum": hl_sum,
        "abs_dclose_sum": abs_dclose_sum,
        "first_break_bar": first_break_bar,
        "i_max": i_max,
        "i_min": i_min
    }
    X.append(feat)
    y.append(c_target)
    ids.append(c["id"])

import pandas as pd
df_X = pd.DataFrame(X)
df_X["C"] = y
df_X["id"] = ids

print("Feature correlations with C:")
corr = df_X.corr(numeric_only=True)["C"].sort_values(ascending=False)
print(corr)
