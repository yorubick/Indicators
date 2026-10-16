import json
import pandas as pd
import numpy as np

d = json.load(open('data/ohlcv_2m_14oct_1400_1450.json'))
# Add 14:52 candle from user report:
# Open: 30,453.25, High: 30,453.50, Low: 30,417.75, Close: 30,418.50, Volume: 3,861
c52 = {
    "time": "2026-10-14T14:52:00.000Z",
    "open": 30453.25,
    "high": 30453.50,
    "low": 30417.75,
    "close": 30418.50,
    "volume": 3861
}
d_ext = d + [c52]
df = pd.DataFrame(d_ext)
df['t_str'] = df['time'].apply(lambda x: x[11:16])

# 4 Windows:
# A: 14:00 to 14:48 (idx 0 to 24, 25 bars) -> C = 128
# B: 14:02 to 14:50 (idx 1 to 25, 25 bars) -> C = 128
# C: 14:00 to 14:50 (idx 0 to 25, 26 bars) -> C = 191
# D: 14:00 to 14:52 (idx 0 to 26, 27 bars) -> C = 195

windows = [
    ("Win A (14:00-14:48)", df.iloc[0:25].copy(), 128),
    ("Win B (14:02-14:50)", df.iloc[1:26].copy(), 128),
    ("Win C (14:00-14:50)", df.iloc[0:26].copy(), 191),
    ("Win D (14:00-14:52)", df.iloc[0:27].copy(), 195),
]

print("=== COMPARATIVA DE LAS 4 VENTANAS EXACTAS ===")
for name, w, c_target in windows:
    n = len(w)
    dt = 120
    t_elap = (n - 1) * dt
    t_inc = n * dt
    
    gh = w['high'].max()
    gl = w['low'].min()
    rng = gh - gl
    
    idx_h = w['high'].idxmax()
    idx_l = w['low'].idxmin()
    time_h = w.loc[idx_h, 't_str']
    time_l = w.loc[idx_l, 't_str']
    
    first = w.iloc[0]
    last = w.iloc[-1]
    
    net_move = last['close'] - first['open']
    tot_vol = w['volume'].sum()
    mean_vol = w['volume'].mean()
    end_vol = last['volume']
    
    c_base = round(t_elap / 18.3)
    delta_c = c_target - c_base
    
    pos = (last['close'] - gl) / rng
    
    print(f"\n{name} -> C = {c_target} (Base={c_base}, Delta={delta_c:+d}s)")
    print(f"  n={n}, T_elap={t_elap}s, T_inc={t_inc}s")
    print(f"  High={gh:.2f} at {time_h}, Low={gl:.2f} at {time_l}, Range={rng:.2f} pts")
    print(f"  Start Open={first['open']}, End Close={last['close']}, Net Move={net_move:.2f}")
    print(f"  Close Pos={pos:.4f}, End Vol={end_vol}, Tot Vol={tot_vol}")
