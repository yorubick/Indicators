import json
import pandas as pd
import numpy as np

# Load 12-Oct
d12 = json.load(open('data/ohlcv_2m_1430_1516.json'))
df12 = pd.DataFrame(d12)

# Load 14-Oct
d14 = json.load(open('data/ohlcv_2m_14oct_1400_1454.json'))
df14 = pd.DataFrame(d14)

# 12 exact cases:
cases = [
    # 12-Oct (START 14:30)
    {'id': '12oct_1510', 'df': df12.iloc[:21], 'dt': 120, 'C': 124},
    {'id': '12oct_1512', 'df': df12.iloc[:22], 'dt': 120, 'C': 153},
    {'id': '12oct_1514', 'df': df12.iloc[:23], 'dt': 120, 'C': 146},
    {'id': '12oct_1516', 'df': df12.iloc[:24], 'dt': 120, 'C': 190},
    # 14-Oct (START 14:00)
    {'id': '14oct_1444', 'df': df14.iloc[:23], 'dt': 120, 'C': 181},
    {'id': '14oct_1446', 'df': df14.iloc[:24], 'dt': 120, 'C': 191},
    {'id': '14oct_1448', 'df': df14.iloc[:25], 'dt': 120, 'C': 128},
    {'id': '14oct_1450', 'df': df14.iloc[:26], 'dt': 120, 'C': 191},
    {'id': '14oct_1452', 'df': df14.iloc[:27], 'dt': 120, 'C': 195},
    {'id': '14oct_1454', 'df': df14.iloc[:28], 'dt': 120, 'C': 177},
    # 14-Oct (START 14:02)
    {'id': '14oct_1402_1450', 'df': df14.iloc[1:26], 'dt': 120, 'C': 128},
    # 14-Oct (START 13:30, END 14:18) -> C = 120
    {'id': '14oct_1330_1418', 'df': None, 'dt': 120, 'C': 120, 'T_elap': 2880, 'n': 25}
]

print("=== TABLA MAESTRA DE LOS 12 CASOS DE 2M ===")
rows = []
for c in cases:
    cid = c['id']
    sub = c['df']
    dt = c['dt']
    c_val = c['C']
    
    if sub is not None:
        n = len(sub)
        t_elap = (n - 1) * dt
        t_inc = n * dt
        gh = sub['high'].max()
        gl = sub['low'].min()
        rng = gh - gl
        first = sub.iloc[0]
        last = sub.iloc[-1]
        net_move = last['close'] - first['open']
        pos = (last['close'] - gl) / rng if rng > 0 else 0.5
        
        idx_h = sub['high'].idxmax()
        idx_l = sub['low'].idxmin()
        bs_h = len(sub) - 1 - idx_h
        bs_l = len(sub) - 1 - idx_l
        span_hl = abs(idx_h - idx_l)
        
        # Volume
        mean_vol = sub['volume'].mean()
        vol_ratio = last['volume'] / mean_vol if mean_vol > 0 else 1.0
    else:
        n = c['n']
        t_elap = c['T_elap']
        t_inc = n * dt
        gh, gl, rng, net_move, pos, bs_h, bs_l, span_hl, vol_ratio = [np.nan]*9
        
    base_elap = round(t_elap / 18.3)
    base_inc = round(t_inc / 18.3)
    delta_elap = c_val - base_elap
    delta_inc = c_val - base_inc
    kappa_elap = round(t_elap / c_val, 3)
    kappa_inc = round(t_inc / c_val, 3)
    
    rows.append({
        'id': cid,
        'n': n,
        'T_elap': t_elap,
        'C': c_val,
        'kappa_elap': kappa_elap,
        'Base_elap': base_elap,
        'Delta_elap': delta_elap,
        'Rng': rng,
        'ClosePos': round(pos, 3) if not np.isnan(pos) else None,
        'bs_H': bs_h,
        'bs_L': bs_l,
        'span_HL': span_hl
    })

res = pd.DataFrame(rows)
print(res.to_string(index=False))
