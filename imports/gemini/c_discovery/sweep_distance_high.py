import json
import pandas as pd
import numpy as np

with open(r"G:\trading\guias\analisis\C_barrido_END_1855_1920_1924_15s.json", "r", encoding="utf-8") as f:
    barrido = json.load(f)

cases = barrido["cases"]

rows = []
for c in cases:
    ohlcv = c["OHLCV"]
    df = pd.DataFrame(ohlcv)
    c_val = c["C_Lite"]
    end = c["END"].split("T")[1][:8]
    
    last = df.iloc[-1]
    r_high = df['high'].max()
    r_low = df['low'].min()
    rng = r_high - r_low
    
    dist_from_high = r_high - last['close']
    dist_from_low = last['close'] - r_low
    pct_pos = dist_from_low / rng
    
    # Also look at last 10, 20 bars
    high_last10 = df['high'].iloc[-10:].max()
    low_last10 = df['low'].iloc[-10:].min()
    dist_h10 = high_last10 - last['close']
    
    rows.append({
        'END': end,
        'C': c_val,
        'close': last['close'],
        'dist_from_high': dist_from_high,
        'pct_pos': pct_pos,
        'dist_h10': dist_h10,
        'volume': last['volume']
    })

res = pd.DataFrame(rows)
print(res.to_string(index=False))
print("\nCorrelation with dist_from_high:")
print("Pearson:", res['dist_from_high'].corr(res['C']))
print("Spearman:", res['dist_from_high'].corr(res['C'], method='spearman'))
