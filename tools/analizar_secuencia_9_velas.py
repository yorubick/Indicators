import json
import pandas as pd
import numpy as np

d = json.load(open('data/ohlcv_2m_14oct_1400_1454.json'))
df = pd.DataFrame(d)

# Measurements map:
# time -> C
c_map = {
    '14:40': 128,
    '14:42': 191,
    '14:44': 181,
    '14:46': 191,
    '14:48': 128,
    '14:50': 191,
    '14:52': 195,
    '14:54': 177,
    '14:56': 195
}

print("=== ANÁLISIS EXHAUSTIVO DE LA SECUENCIA DE 9 VELAS (14:40 A 14:56) ===")
rows = []
for i in range(20, len(df)):
    row = df.iloc[i]
    t_str = row['time'][11:16]
    c_val = c_map.get(t_str, None)
    
    sub = df.iloc[:i+1]
    prev = df.iloc[:i]
    
    box_h = sub['high'].max()
    box_l = sub['low'].min()
    box_rng = box_h - box_l
    
    prev_h = prev['high'].max()
    prev_l = prev['low'].min()
    
    new_h = row['high'] > prev_h
    new_l = row['low'] < prev_l
    
    bar_rng = row['high'] - row['low']
    bar_body = row['close'] - row['open']
    
    # Distance to box low and box high
    dist_to_l = row['close'] - box_l
    dist_to_h = box_h - row['close']
    pos_in_box = dist_to_l / box_rng if box_rng > 0 else 0.5
    
    rows.append({
        'time': t_str,
        'C': c_val,
        'O': row['open'],
        'H': row['high'],
        'L': row['low'],
        'Close': row['close'],
        'Body': round(bar_body, 2),
        'BarRng': round(bar_rng, 2),
        'PosInBox': round(pos_in_box, 3),
        'NewH': new_h,
        'NewL': new_l,
        'Vol': row['volume']
    })

res = pd.DataFrame(rows)
print(res.to_string(index=False))
