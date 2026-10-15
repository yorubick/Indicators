import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = [c for c in master['cases'] if c['bars'] >= 21 and c.get('C_Lite') is not None]

ratios = [(c['bars'] * c['dt']) / round(c['C_Lite']) for c in cases]

df = pd.DataFrame({'ratio': ratios})
print("Summary of (n * dt) / C across all 110 long Lite cases:")
print(df['ratio'].describe())

# Histogram of ratios
counts, bins = np.histogram(ratios, bins=20)
for i in range(len(counts)):
    print(f"[{bins[i]:.2f} - {bins[i+1]:.2f}]: {counts[i]} cases")
