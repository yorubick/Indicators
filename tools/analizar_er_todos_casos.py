import json
import pandas as pd
import numpy as np

# Load datasets
d14 = json.load(open('data/ohlcv_2m_14oct_1400_1454.json'))
df14 = pd.DataFrame(d14)

d12 = json.load(open('data/ohlcv_2m_1430_1516.json'))
df12 = pd.DataFrame(d12)

d15 = json.load(open('data/ohlcv_2m_15oct_1400_1456.json'))
df15 = pd.DataFrame(d15)

cases = [
    # 15-Oct
    {'name': '15-Oct 14:56', 'df': df15.iloc[:29], 'C': 227},
    # 14-Oct sweep
    {'name': '14-Oct 14:40', 'df': df14.iloc[:21], 'C': 128},
    {'name': '14-Oct 14:42', 'df': df14.iloc[:22], 'C': 191},
    {'name': '14-Oct 14:44', 'df': df14.iloc[:23], 'C': 181},
    {'name': '14-Oct 14:46', 'df': df14.iloc[:24], 'C': 191},
    {'name': '14-Oct 14:48', 'df': df14.iloc[:25], 'C': 128},
    {'name': '14-Oct 14:50', 'df': df14.iloc[:26], 'C': 191},
    {'name': '14-Oct 14:52', 'df': df14.iloc[:27], 'C': 195},
    {'name': '14-Oct 14:54', 'df': df14.iloc[:28], 'C': 177},
    # 12-Oct sweep
    {'name': '12-Oct 15:10', 'df': df12.iloc[:21], 'C': 124},
    {'name': '12-Oct 15:12', 'df': df12.iloc[:22], 'C': 153},
    {'name': '12-Oct 15:14', 'df': df12.iloc[:23], 'C': 146},
    {'name': '12-Oct 15:16', 'df': df12.iloc[:24], 'C': 190},
]

rows = []
for c in cases:
    sub = c['df']
    n = len(sub)
    T = (n - 1) * 120
    C_act = c['C']
    kappa = T / C_act
    
    gh = sub['high'].max()
    gl = sub['low'].min()
    rng = gh - gl
    
    first = sub.iloc[0]
    last = sub.iloc[-1]
    net_move = abs(last['close'] - first['open'])
    path = np.abs(sub['close'].diff()).sum()
    er = net_move / path if path > 0 else 0
    net_to_rng = net_move / rng if rng > 0 else 0
    
    pos = (last['close'] - gl) / rng if rng > 0 else 0.5
    
    # Volume
    vol_mean = sub['volume'].mean()
    vol_tot = sub['volume'].sum()
    
    rows.append({
        'Case': c['name'],
        'n': n,
        'T': T,
        'C': C_act,
        'kappa': round(kappa, 2),
        'Range': round(rng, 2),
        'NetMove': round(net_move, 2),
        'ER': round(er, 3),
        'Net/Rng': round(net_to_rng, 3),
        'Pos': round(pos, 3)
    })

res = pd.DataFrame(rows)
print(res.to_string(index=False))
