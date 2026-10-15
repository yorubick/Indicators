import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = [c for c in master['cases'] if c['bars'] >= 21 and c.get('C_Lite') is not None]

# Check how well floor(n * dt / 18.0) vs floor(n * dt / 18.3) correlates across all 110 cases
df = pd.DataFrame([{
    'id': c['id'],
    'n': c['bars'],
    'dt': c['dt'],
    'C': round(c['C_Lite']),
    'floor_18': int(np.floor(c['bars'] * c['dt'] / 18.0)),
    'floor_183': int(np.floor(c['bars'] * c['dt'] / 18.3)),
    'round_183': int(round(c['bars'] * c['dt'] / 18.3)),
} for c in cases])

df['err_floor_18'] = df['C'] - df['floor_18']
df['err_floor_183'] = df['C'] - df['floor_183']
df['err_round_183'] = df['C'] - df['round_183']

print("Global Metrics on All 110 Long Lite Cases:")
print(f"Mean Abs Error (floor 18.0): {df['err_floor_18'].abs().mean():.2f}, Mean bias: {df['err_floor_18'].mean():.2f}")
print(f"Mean Abs Error (floor 18.3): {df['err_floor_183'].abs().mean():.2f}, Mean bias: {df['err_floor_183'].mean():.2f}")
print(f"Mean Abs Error (round 18.3): {df['err_round_183'].abs().mean():.2f}, Mean bias: {df['err_round_183'].mean():.2f}")

# Look at 15s cases specifically
df_15 = df[df['dt'] == 15]
print(f"\n15s Cases (N = {len(df_15)}):")
print(f"Mean bias floor 18.0: {df_15['err_floor_18'].mean():.2f}")
print(f"Mean bias floor 18.3: {df_15['err_floor_183'].mean():.2f}")
print(f"Mean bias round 18.3: {df_15['err_round_183'].mean():.2f}")
