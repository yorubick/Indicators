import pandas as pd
import numpy as np
from deep_inspect_candles import df, start_idx

# Load the 13 measurements
import json
with open(r"C:\Users\PC\.gemini\antigravity\scratch\c_discovery\serie_1903_mediciones_completas.json", "r") as f:
    cases = json.load(f)

# Let's inspect each window [START..END]
# For each window, we evaluate what pivots exist strictly INSIDE the window [START..END]
# For radius L in {1, 2}:
# A pivot high at index k inside window [0..n-1] is confirmed if:
# - k >= L
# - k <= n - 1 - L (i.e. there are at least L bars after k inside the window)
# - high[k] > high[k-j] for j in 1..L
# - high[k] > high[k+j] for j in 1..L

print("=== PIVOT AUDIT FOR 13 WINDOWS (START 19:03) ===")

for L in [1, 2]:
    print(f"\n--- RADIUS L = {L} ---")
    for c in cases:
        end_m = c["END"]
        c_val = c["C"]
        n = c["n"]
        end_i = df[df["time_str"] == end_m].index[0]
        w = df.iloc[start_idx : end_i + 1].copy().reset_index(drop=True)
        
        highs = w["high"].values
        lows = w["low"].values
        times = w["time_str"].values
        
        piv_h = []
        piv_l = []
        for k in range(L, len(w) - L):
            if all(highs[k] > highs[k-j] for j in range(1, L+1)) and all(highs[k] >= highs[k+j] for j in range(1, L+1)):
                piv_h.append((times[k], highs[k], len(w) - 1 - k)) # (time, price, bars_ago)
            if all(lows[k] < lows[k-j] for j in range(1, L+1)) and all(lows[k] <= lows[k+j] for j in range(1, L+1)):
                piv_l.append((times[k], lows[k], len(w) - 1 - k))
                
        last_ph = piv_h[-1] if piv_h else ("None", 0, -1)
        last_pl = piv_l[-1] if piv_l else ("None", 0, -1)
        
        # Check if END bar broke the last confirmed pivot high
        end_high = highs[-1]
        end_close = w.iloc[-1]["close"]
        broke_last_ph_by_high = end_high > last_ph[1] if last_ph[0] != "None" else False
        broke_last_ph_by_close = end_close > last_ph[1] if last_ph[0] != "None" else False
        
        print(f"END {end_m} (n={n:2d}) | C={c_val:3d} | Last PH: {last_ph[0]} ({last_ph[1]:.2f}, {last_ph[2]:2d}b ago) | Last PL: {last_pl[0]} ({last_pl[1]:.2f}, {last_pl[2]:2d}b ago) | BrkH:{broke_last_ph_by_high} BrkC:{broke_last_ph_by_close}")
