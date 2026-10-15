import json
import pandas as pd
import numpy as np

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

cases21 = [c for c in master["cases"] if c.get("bars") == 21]
print(f"Total cases with bars == 21: {len(cases21)}")

rows = []
for c in cases21:
    df = pd.DataFrame(c["OHLCV"])
    dt = c["dt"]
    c_val = c.get("C_Lite") if c.get("C_Lite") is not None else c.get("C")
    
    high = df['high'].max()
    low = df['low'].min()
    rng = high - low
    
    # Let's find index of high and low
    idx_h = df['high'].argmax()
    idx_l = df['low'].argmin()
    
    # Close start, end
    c_start = df.iloc[0]['close']
    c_end = df.iloc[-1]['close']
    net = c_end - c_start
    
    # Path length
    path = np.sum(np.abs(np.diff(df['close'])))
    
    # True range
    tr = np.maximum(df['high'].iloc[1:].values - df['low'].iloc[1:].values,
                    np.maximum(np.abs(df['high'].iloc[1:].values - df['close'].iloc[:-1].values),
                               np.abs(df['low'].iloc[1:].values - df['close'].iloc[:-1].values)))
    atr = np.mean(tr)
    
    rows.append({
        'id': c['id'],
        'dt': dt,
        'C': c_val,
        'high': high,
        'low': low,
        'rng': rng,
        'idx_h': idx_h,
        'idx_l': idx_l,
        'net': net,
        'path': path,
        'atr': atr,
        'c_end': c_end
    })

res = pd.DataFrame(rows)
print(res.to_string(index=False))
