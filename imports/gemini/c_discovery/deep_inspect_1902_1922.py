import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = {c['id']: c for c in master['cases']}

# Let's inspect 1902_1922_60s
c50 = cases['20261012_190200_192200_60s']
c77_22 = cases.get('20261012_190100_192200_60s')
c77_21 = cases.get('20261012_190100_192100_60s')

print("Case 1902_1922 (C=50):")
df50 = pd.DataFrame(c50['OHLCV'])
df50['dt_min'] = (df50['time'] - df50['time'].iloc[0]) / 60
print(df50[['dt_min', 'open', 'high', 'low', 'close', 'volume']])

# Let's examine price differences, swings, etc.
# Price range:
rng = df50['high'].max() - df50['low'].min()
print(f"Range: {rng} pts = {rng*4} ticks")

# High and Low indices:
h_idx = df50['high'].idxmax()
l_idx = df50['low'].idxmin()
print(f"High at index {h_idx} (min {df50['dt_min'].iloc[h_idx]}): {df50['high'].max()}")
print(f"Low at index {l_idx} (min {df50['dt_min'].iloc[l_idx]}): {df50['low'].min()}")

# Distance between Low and High:
print(f"Index distance between Low and High: {abs(h_idx - l_idx)} bars = {abs(h_idx - l_idx)*60} s")
print(f"Distance from Low to END: {len(df50) - 1 - l_idx} bars = {(len(df50) - 1 - l_idx)*60} s")
print(f"Distance from START to High: {h_idx} bars = {h_idx*60} s")
print(f"Distance from START to Low: {l_idx} bars = {l_idx*60} s")
