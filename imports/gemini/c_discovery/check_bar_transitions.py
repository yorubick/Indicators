import pandas as pd
from deep_inspect_candles import res, df, start_idx

print("=== INSPECTING LOW[i] < LOW[i-1] and HIGH[i] > HIGH[i-1] ===")

# For each bar from 19:23 to 19:35:
for idx, r in res.iterrows():
    m = r["END"]
    c_val = r["C"]
    end_i = df[df["time_str"] == m].index[0]
    
    curr_bar = df.iloc[end_i]
    prev_bar = df.iloc[end_i - 1]
    prev2_bar = df.iloc[end_i - 2]
    
    higher_high = curr_bar["high"] > prev_bar["high"]
    higher_low  = curr_bar["low"] > prev_bar["low"]
    lower_low   = curr_bar["low"] < prev_bar["low"]
    lower_high  = curr_bar["high"] < prev_bar["high"]
    inside_bar  = (curr_bar["high"] <= prev_bar["high"]) and (curr_bar["low"] >= prev_bar["low"])
    outside_bar = (curr_bar["high"] > prev_bar["high"]) and (curr_bar["low"] < prev_bar["low"])
    
    # Distance of low to previous low
    delta_low = curr_bar["low"] - prev_bar["low"]
    delta_high = curr_bar["high"] - prev_bar["high"]
    
    print(f"END {m} (n={r['n']:2d}) | C={c_val:3d} | HH:{higher_high} HL:{higher_low} LL:{lower_low} Inside:{inside_bar} Outside:{outside_bar} | dH:{delta_high:+6.2f} dL:{delta_low:+6.2f}")
