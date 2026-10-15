import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = master['cases']

rows = []
for c in cases:
    n = c['bars']
    dt = c['dt']
    total_sec = n * dt
    c_val = c.get('C_Lite')
    if c_val is None:
        c_val = c['C_Character_interval']['lower_inclusive']
    
    pred_short = max(dt, total_sec * 10.0 / 183.0)
    pred_short_round = round(pred_short)
    
    diff = c_val - pred_short
    diff_round = round(c_val) - pred_short_round
    
    rows.append({
        'id': c['id'],
        'dt': dt,
        'n': n,
        'total_sec': total_sec,
        'C': c_val,
        'C_round': round(c_val),
        'pred_short': pred_short,
        'pred_round': pred_short_round,
        'diff': diff,
        'diff_round': diff_round
    })

df = pd.DataFrame(rows)
df_short = df[df['n'] < 21]
df_long = df[df['n'] >= 21]

print("SHORT REGIME (n < 21):")
print(f"Max abs diff: {abs(df_short['diff']).max()}")

print("\nLONG REGIME (n >= 21):")
print(f"Mean diff: {df_long['diff'].mean():.2f}, std diff: {df_long['diff'].std():.2f}")
print("Diff distribution (diff_round):")
print(df_long['diff_round'].value_counts().sort_index())
