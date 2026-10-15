import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

rows = []
for c in data['cases']:
    if c['bars'] >= 21 and c['dt'] == 60:
        c_val = round(c['C'])
        rem = c_val % 3
        # rem = 0 -> Lattice 1 (3Z)
        # rem = 2 -> Lattice 2 (3Z - 1)
        # rem = 1 -> other (3Z + 1)
        ohlc = c['OHLC']
        highs = [x['high'] for x in ohlc]
        lows = [x['low'] for x in ohlc]
        opens = [x['open'] for x in ohlc]
        closes = [x['close'] for x in ohlc]
        rng = max(highs) - min(lows)
        sp = (opens[0] - min(lows)) / rng if rng > 0 else 0.5
        ep = (closes[-1] - min(lows)) / rng if rng > 0 else 0.5
        
        rows.append({
            'id': c['id'][:26],
            'bars': c['bars'],
            'C': c_val,
            'rem3': rem,
            'lattice': '3Z' if rem == 0 else ('3Z-1' if rem == 2 else '3Z+1'),
            'rng': round(rng, 2),
            'sp': round(sp, 2),
            'ep': round(ep, 2),
            'split': c['split']
        })

df = pd.DataFrame(rows)
print("=== LATTICE DISTRIBUTION ===")
print(df['lattice'].value_counts())
print("\n=== LATTICE BY ID ===")
print(df.to_string())
