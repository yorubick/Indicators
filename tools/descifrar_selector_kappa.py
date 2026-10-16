import json
import pandas as pd
import numpy as np

d12 = json.load(open('data/ohlcv_2m_1430_1516.json'))
df12 = pd.DataFrame(d12)

d14 = json.load(open('data/ohlcv_2m_14oct_1400_1454.json'))
df14 = pd.DataFrame(d14)

# The 5 states of kappa:
# State 5: kappa = 24.0 (Apertura RTH, Floor clamping)
# State 4: kappa = 22.5 (Compresión / consolidación dentro de rango: 14:48)
# State 3: kappa = 18.3 (Base Pura / Reversión / Absorción: 14:54)
# State 2: kappa = 16.0 (Expansión moderada: 14:52, 12-Oct 15:12)
# State 1: kappa = 14.5 (Expansión máxima / Ruptura fuerte: 14:44, 14:46, 14:50, 12-Oct 15:16)

cases_to_compare = [
    {'name': '14:48 (kappa=22.5)', 'sub': df14.iloc[:25], 'kappa': 22.5},
    {'name': '14:54 (kappa=18.3)', 'sub': df14.iloc[:28], 'kappa': 18.3},
    {'name': '14:52 (kappa=16.0)', 'sub': df14.iloc[:27], 'kappa': 16.0},
    {'name': '14:50 (kappa=15.7)', 'sub': df14.iloc[:26], 'kappa': 15.7},
    {'name': '14:46 (kappa=14.5)', 'sub': df14.iloc[:24], 'kappa': 14.5},
    {'name': '14:44 (kappa=14.5)', 'sub': df14.iloc[:23], 'kappa': 14.5},
    {'name': '12-Oct 15:16 (kappa=14.5)', 'sub': df12.iloc[:24], 'kappa': 14.5},
    {'name': '12-Oct 15:12 (kappa=16.5)', 'sub': df12.iloc[:22], 'kappa': 16.5},
    {'name': '12-Oct 15:14 (kappa=18.1)', 'sub': df12.iloc[:23], 'kappa': 18.1},
    {'name': '12-Oct 15:10 (kappa=19.4)', 'sub': df12.iloc[:21], 'kappa': 19.4},
]

print("=== ANÁLISIS DE CONDICIONES ESTRUCTURALES DE LOS 5 ESTADOS DE KAPPA ===")
rows = []
for c in cases_to_compare:
    sub = c['sub']
    k_target = c['kappa']
    name = c['name']
    
    n = len(sub)
    gh = sub['high'].max()
    gl = sub['low'].min()
    rng = gh - gl
    
    last = sub.iloc[-1]
    prev = sub.iloc[-2]
    
    # Check if last bar broke high or low of previous range
    prev_gh = sub.iloc[:-1]['high'].max()
    prev_gl = sub.iloc[:-1]['low'].min()
    new_h = last['high'] > prev_gh
    new_l = last['low'] < prev_gl
    
    # Position in range
    pos = (last['close'] - gl) / rng
    
    # Last bar characteristics
    last_rng = last['high'] - last['low']
    last_body = last['close'] - last['open']
    body_ratio = abs(last_body) / last_rng if last_rng > 0 else 0
    
    # Upper/lower wicks
    uw = last['high'] - max(last['open'], last['close'])
    lw = min(last['open'], last['close']) - last['low']
    uw_ratio = uw / last_rng if last_rng > 0 else 0
    lw_ratio = lw / last_rng if last_rng > 0 else 0
    
    # Path & Net move
    net_move = abs(last['close'] - sub.iloc[0]['open'])
    path = np.abs(sub['close'].diff()).sum()
    er = net_move / path if path > 0 else 0
    
    # Distance to extremes in bars
    idx_h = sub['high'].idxmax()
    idx_l = sub['low'].idxmin()
    bs_h = n - 1 - idx_h
    bs_l = n - 1 - idx_l
    dist_ext_bars = min(bs_h, bs_l)
    
    rows.append({
        'name': name,
        'kappa': k_target,
        'Rng': rng,
        'new_H': new_h,
        'new_L': new_l,
        'bs_ext': dist_ext_bars,
        'pos': round(pos, 3),
        'body_rt': round(body_ratio, 2),
        'uw_rt': round(uw_ratio, 2),
        'lw_rt': round(lw_ratio, 2),
        'ER': round(er, 3)
    })

res = pd.DataFrame(rows)
print(res.to_string(index=False))
