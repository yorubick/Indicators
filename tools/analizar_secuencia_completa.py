import json
import pandas as pd
import numpy as np

d = json.load(open('data/ohlcv_2m_14oct_1400_1450.json'))
# 14:52 from user report:
c52 = {
    "time": "2026-10-14T14:52:00.000Z",
    "open": 30453.25,
    "high": 30453.50,
    "low": 30417.75,
    "close": 30418.50,
    "volume": 3861
}
# We don't have 14:54 full candle yet, but we know C = 177
df = pd.DataFrame(d + [c52])
df['t_str'] = df['time'].apply(lambda x: x[11:16])

c_measured = {
    '14:44': 181,
    '14:46': 191,
    '14:48': 128,
    '14:50': 191,
    '14:52': 195,
    '14:54': 177
}

print("=== SECUENCIA DE 6 VELAS EN 14-OCT (START 14:00) ===")
rows = []
for i in range(21, len(df)):
    r = df.iloc[i]
    t = r['t_str']
    c_val = c_measured.get(t)
    
    # Sub-dataframe up to this candle
    sub = df.iloc[:i+1]
    n_inc = len(sub)
    n_elap = n_inc - 1
    t_elap = n_elap * 120
    
    base_elap = round(t_elap / 18.3)
    delta_elap = c_val - base_elap if c_val else None
    
    gh = sub['high'].max()
    gl = sub['low'].min()
    rng = gh - gl
    
    idx_h = sub['high'].idxmax()
    idx_l = sub['low'].idxmin()
    bs_h = i - idx_h
    bs_l = i - idx_l
    
    c = r['close']
    o = r['open']
    h = r['high']
    l = r['low']
    body = c - o
    c_rng = h - l
    
    pos = (c - gl) / rng
    
    rows.append({
        'time': t,
        'C': c_val,
        'Base': base_elap,
        'Delta': delta_elap,
        'O': o, 'H': h, 'L': l, 'Close': c, 'Vol': r['volume'],
        'body': body,
        'rng': c_rng,
        'GH': gh, 'GL': gl, 'bs_H': bs_h, 'bs_L': bs_l,
        'ClosePos': round(pos, 3)
    })

res = pd.DataFrame(rows)
print(res.to_string(index=False))
