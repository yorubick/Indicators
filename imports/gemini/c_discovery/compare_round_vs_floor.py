import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = master['cases']
long_cases = [c for c in cases if c['bars'] >= 21 and c.get('C_Lite') is not None]

rows = []
for c in long_cases:
    n = c['bars']
    dt = c['dt']
    c_val = round(c['C_Lite'])
    val_cont = n * dt * 10.0 / 183.0
    val_round = round(val_cont)
    val_floor = int(np.floor(val_cont))
    val_ceil = int(np.ceil(val_cont))
    
    rows.append({
        'id': c['id'],
        'dt': dt,
        'n': n,
        'C': c_val,
        'cont': val_cont,
        'round': val_round,
        'floor': val_floor,
        'ceil': val_ceil,
        'diff_round': c_val - val_round,
        'diff_floor': c_val - val_floor,
    })

df = pd.DataFrame(rows)
print("Comparison across all 110 long Lite cases:")
print(f"Mean diff (C - round): {df['diff_round'].mean():.2f}, std: {df['diff_round'].std():.2f}")
print(f"Mean diff (C - floor): {df['diff_floor'].mean():.2f}, std: {df['diff_floor'].std():.2f}")
print(f"Exact matches with round: {(df['diff_round'] == 0).sum()} / 110")
print(f"Exact matches with floor: {(df['diff_floor'] == 0).sum()} / 110")

print("\nSample near boundary cases:")
boundary_cases = df[df['n'].isin([21, 22, 23])][['id', 'dt', 'n', 'C', 'cont', 'round', 'floor', 'diff_round', 'diff_floor']]
print(boundary_cases.head(15).to_string(index=False))
