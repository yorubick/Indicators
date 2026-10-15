import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = [c for c in master['cases'] if c['bars'] >= 21 and c.get('C_Lite') is not None]

diffs = [round(c['C_Lite']) - int(round(c['bars'] * c['dt'] / 18.3)) for c in cases]

df = pd.DataFrame({'diff': diffs})
print("Residuals C - round(n*dt / 18.3):")
print(f"Mean: {df['diff'].mean():.2f}")
print(f"Median: {df['diff'].median():.2f}")
print(f"Std: {df['diff'].std():.2f}")
print(f"Values within +/- 5s: {(df['diff'].abs() <= 5).sum()} / {len(df)} ({(df['diff'].abs() <= 5).mean()*100:.1f}%)")
print(f"Values within +/- 9s: {(df['diff'].abs() <= 9).sum()} / {len(df)} ({(df['diff'].abs() <= 9).mean()*100:.1f}%)")
print(f"Values within +/- 18s: {(df['diff'].abs() <= 18).sum()} / {len(df)} ({(df['diff'].abs() <= 18).mean()*100:.1f}%)")
print(f"Values within +/- 27s: {(df['diff'].abs() <= 27).sum()} / {len(df)} ({(df['diff'].abs() <= 27).mean()*100:.1f}%)")
