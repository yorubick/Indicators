import json
import numpy as np
import pandas as pd

with open(r"G:\trading\guias\analisis\C_barrido_END_1855_1920_1924_15s.json", "r", encoding="utf-8") as f:
    barrido = json.load(f)

cases = barrido["cases"]

print(f"Total barrido cases: {len(cases)}")

# Let's inspect each case
rows = []
for i, c in enumerate(cases):
    ohlcv = c["OHLCV"]
    c_val = c["C_Lite"]
    end = c["END"]
    df = pd.DataFrame(ohlcv)
    
    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last
    
    # Range stats
    r_high = df['high'].max()
    r_low = df['low'].min()
    r_open = df.iloc[0]['open']
    r_close = last['close']
    r_vol = df['volume'].sum()
    
    # Distance of last bar to range extremes
    dist_high = r_high - last['high']
    dist_low = last['low'] - r_low
    dist_close_high = r_high - last['close']
    dist_close_low = last['close'] - r_low
    
    rows.append({
        'step': i,
        'END': end.split("T")[1][:8],
        'n': len(df),
        'C': c_val,
        'O': last['open'],
        'H': last['high'],
        'L': last['low'],
        'Close': last['close'],
        'V': last['volume'],
        'cumV': r_vol,
        'r_H': r_high,
        'r_L': r_low,
        'new_H': last['high'] >= df.iloc[:-1]['high'].max(),
        'new_L': last['low'] <= df.iloc[:-1]['low'].min(),
        'body': last['close'] - last['open'],
        'range': last['high'] - last['low'],
    })

res_df = pd.DataFrame(rows)
print(res_df.to_string(index=False))
