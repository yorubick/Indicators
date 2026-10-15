import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = {c['id']: c for c in master['cases']}

c88 = cases['20261012_190315_192345_15s']
c61 = cases['20261012_190330_192345_15s']

df88 = pd.DataFrame(c88['OHLCV'])
df61 = pd.DataFrame(c61['OHLCV'])

# Let's inspect all local highs and lows (pivots of radius 1, 2, 3)
for r in [1, 2]:
    highs = []
    lows = []
    for i in range(r, len(df88) - r):
        if all(df88['high'].iloc[i] > df88['high'].iloc[i-k] for k in range(1, r+1)) and \
           all(df88['high'].iloc[i] >= df88['high'].iloc[i+k] for k in range(1, r+1)):
            highs.append((i, df88.iloc[i]['time'], df88.iloc[i]['high']))
        if all(df88['low'].iloc[i] < df88['low'].iloc[i-k] for k in range(1, r+1)) and \
           all(df88['low'].iloc[i] <= df88['low'].iloc[i+k] for k in range(1, r+1)):
            lows.append((i, df88.iloc[i]['time'], df88.iloc[i]['low']))
    print(f"\nRadius {r} pivots for C88:")
    print("Highs count:", len(highs), "Lows count:", len(lows))
    print("First 3 highs:", highs[:3])
    print("First 3 lows:", lows[:3])
    print("Last 3 highs:", highs[-3:])
    print("Last 3 lows:", lows[-3:])
