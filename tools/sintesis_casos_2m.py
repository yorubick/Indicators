import json
import pandas as pd
import numpy as np

# Load 14-Oct
d14 = json.load(open('data/ohlcv_2m_14oct_1400_1454.json'))
df14 = pd.DataFrame(d14)

# Load 12-Oct
d12 = json.load(open('data/ohlcv_2m_1430_1516.json'))
df12 = pd.DataFrame(d12)

# Full set of exact 2m cases:
all_cases = [
    # 14-Oct sequence (START 14:00)
    {'date': '14-Oct', 'end_t': '14:40', 'n': 21, 'T': 2400, 'C': 128, 'df': df14.iloc[:21]},
    {'date': '14-Oct', 'end_t': '14:42', 'n': 22, 'T': 2520, 'C': 191, 'df': df14.iloc[:22]},
    {'date': '14-Oct', 'end_t': '14:44', 'n': 23, 'T': 2640, 'C': 181, 'df': df14.iloc[:23]},
    {'date': '14-Oct', 'end_t': '14:46', 'n': 24, 'T': 2760, 'C': 191, 'df': df14.iloc[:24]},
    {'date': '14-Oct', 'end_t': '14:48', 'n': 25, 'T': 2880, 'C': 128, 'df': df14.iloc[:25]},
    {'date': '14-Oct', 'end_t': '14:50', 'n': 26, 'T': 3000, 'C': 191, 'df': df14.iloc[:26]},
    {'date': '14-Oct', 'end_t': '14:52', 'n': 27, 'T': 3120, 'C': 195, 'df': df14.iloc[:27]},
    {'date': '14-Oct', 'end_t': '14:54', 'n': 28, 'T': 3240, 'C': 177, 'df': df14.iloc[:28]},
    # 14-Oct other windows
    {'date': '14-Oct', 'end_t': '14:50 (st 14:02)', 'n': 25, 'T': 2880, 'C': 128, 'df': df14.iloc[1:26]},
    {'date': '14-Oct', 'end_t': '14:18 (st 13:30)', 'n': 25, 'T': 2880, 'C': 120, 'df': None}, # RTH open floor
    # 12-Oct cases (START 14:30)
    {'date': '12-Oct', 'end_t': '15:10', 'n': 21, 'T': 2400, 'C': 124, 'df': df12.iloc[:21]},
    {'date': '12-Oct', 'end_t': '15:12', 'n': 22, 'T': 2520, 'C': 153, 'df': df12.iloc[:22]},
    {'date': '12-Oct', 'end_t': '15:14', 'n': 23, 'T': 2640, 'C': 146, 'df': df12.iloc[:23]},
    {'date': '12-Oct', 'end_t': '15:16', 'n': 24, 'T': 2760, 'C': 190, 'df': df12.iloc[:24]}
]

print("=== SÍNTESIS DE TODOS LOS CASOS EXACTOS EN 2M ===")
rows = []
for c in all_cases:
    if c['df'] is None:
        continue
    sub = c['df']
    n = len(sub)
    T = (n - 1) * 120
    C_actual = c['C']
    kappa = T / C_actual
    C_base = round(T / 18.3)
    delta_C = C_actual - C_base
    k_mult_9 = delta_C / 9.0
    
    gh = sub['high'].max()
    gl = sub['low'].min()
    rng = gh - gl
    last = sub.iloc[-1]
    prev_gh = sub.iloc[:-1]['high'].max()
    prev_gl = sub.iloc[:-1]['low'].min()
    new_h = last['high'] > prev_gh
    new_l = last['low'] < prev_gl
    pos = (last['close'] - gl) / rng
    
    rows.append({
        'Date': c['date'],
        'End': c['end_t'],
        'n': n,
        'T': T,
        'C': C_actual,
        'kappa': round(kappa, 2),
        'Base': C_base,
        'DeltaC': delta_C,
        'k_9s': round(k_mult_9, 2),
        'Rng': round(rng, 2),
        'Pos': round(pos, 3),
        'NewExt': new_h or new_l
    })

df_res = pd.DataFrame(rows)
print(df_res.to_string(index=False))
