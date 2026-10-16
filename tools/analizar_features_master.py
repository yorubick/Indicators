import json
import pandas as pd
import numpy as np

data = json.load(open('master_all_C_cases.json'))
cases = data['cases']
ge21 = [c for c in cases if c['bars'] >= 21]

rows = []
for c in ge21:
    bars = c['OHLCV'] if 'OHLCV' in c and c['OHLCV'] else c['OHLC']
    df = pd.DataFrame(bars)
    n = len(df)
    dt = c['dt']
    t_elap = (n - 1) * dt
    t_inc = n * dt
    c_val = c['C']
    
    gh = df['high'].max()
    gl = df['low'].min()
    rng = gh - gl
    
    first = df.iloc[0]
    last = df.iloc[-1]
    
    net_move = abs(last['close'] - first['open'])
    path = np.abs(df['close'].diff()).sum()
    er = net_move / path if path > 0 else 0
    
    pos = (last['close'] - gl) / rng if rng > 0 else 0.5
    
    # Distance in bars to high and low
    idx_h = df['high'].idxmax()
    idx_l = df['low'].idxmin()
    bs_h = n - 1 - idx_h
    bs_l = n - 1 - idx_l
    
    # Volume features if present
    vol_last = last['volume'] if 'volume' in last else 0
    vol_mean = df['volume'].mean() if 'volume' in df else 0
    vol_ratio = vol_last / vol_mean if vol_mean > 0 else 1.0
    
    kappa_elap = t_elap / c_val if c_val > 0 else 0
    kappa_inc = t_inc / c_val if c_val > 0 else 0
    
    rows.append({
        'id': c['id'],
        'n': n,
        'dt': dt,
        'T_elap': t_elap,
        'T_inc': t_inc,
        'C': c_val,
        'kappa_elap': kappa_elap,
        'kappa_inc': kappa_inc,
        'rng': rng,
        'net_move': net_move,
        'er': er,
        'pos': pos,
        'bs_h': bs_h,
        'bs_l': bs_l,
        'min_bs_ext': min(bs_h, bs_l),
        'vol_ratio': vol_ratio
    })

res = pd.DataFrame(rows)
print("=== CORRELACIONES CON KAPPA_ELAP ===")
corr = res[['kappa_elap', 'T_elap', 'rng', 'net_move', 'er', 'pos', 'min_bs_ext', 'vol_ratio']].corr()
print(corr['kappa_elap'])

print("\n=== CORRELACIONES CON C ===")
corr_c = res[['C', 'T_elap', 'rng', 'net_move', 'er', 'pos', 'min_bs_ext', 'vol_ratio']].corr()
print(corr_c['C'])
