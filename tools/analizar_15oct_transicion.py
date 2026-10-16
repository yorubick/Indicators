import json
import pandas as pd
import numpy as np

d15 = json.load(open('data/ohlcv_2m_15oct_1400_1456.json'))
df15 = pd.DataFrame(d15)

print("=== VELAS DEL 15 DE OCTUBRE ENTRE 14:40 Y 14:56 ===")
for i in range(20, len(df15)):
    r = df15.iloc[i]
    t_str = r['time'][11:16]
    n = i + 1
    t_elap = i * 120
    
    # Cumulative range up to this bar
    sub = df15.iloc[:i+1]
    gh = sub['high'].max()
    gl = sub['low'].min()
    rng = gh - gl
    
    # Check if this bar made new high or low
    prev_gh = df15.iloc[:i]['high'].max()
    prev_gl = df15.iloc[:i]['low'].min()
    new_h = r['high'] > prev_gh
    new_l = r['low'] < prev_gl
    
    print(f"{t_str} (n={n}, T={t_elap}s): O={r['open']:.2f}, H={r['high']:.2f}, L={r['low']:.2f}, Close={r['close']:.2f}, Range={rng:.2f}, NewH={new_h}, NewL={new_l}, Vol={r['volume']}")
