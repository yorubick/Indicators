import pandas as pd
import numpy as np
from deep_inspect_candles import res, df, start_idx

# Let's inspect the entire window for each END:
# What about pivots? Radii 1, 2, 3 pivots?
# What about time since last confirmed swing high/low?
# What about the breakout bar itself?

for idx, r in res.iterrows():
    m = r["END"]
    c_val = r["C"]
    end_i = df[df["time_str"] == m].index[0]
    w = df.iloc[start_idx : end_i + 1]
    
    # Let's check pivots of radius 1 (high[i] > high[i-1] and high[i] > high[i+1])
    # within the window
    highs = w["high"].values
    lows = w["low"].values
    times = w["time_str"].values
    
    piv_h = []
    piv_l = []
    for i in range(1, len(w) - 1):
        if highs[i] > highs[i-1] and highs[i] > highs[i+1]:
            piv_h.append((times[i], highs[i], len(w) - 1 - i))
        if lows[i] < lows[i-1] and lows[i] < lows[i+1]:
            piv_l.append((times[i], lows[i], len(w) - 1 - i))
            
    last_piv_h = piv_h[-1] if piv_h else None
    last_piv_l = piv_l[-1] if piv_l else None
    
    print(f"END {m:5} | C={c_val:3d} | Last Piv H: {str(last_piv_h):30} | Last Piv L: {str(last_piv_l):30}")
