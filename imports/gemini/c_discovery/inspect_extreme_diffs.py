import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = [c for c in master['cases'] if c['bars'] >= 21 and c.get('C_Lite') is not None]

rows = []
for c in cases:
    n = c['bars']
    dt = c['dt']
    C = round(c['C_Lite'])
    expected_cont = n * dt / 18.3
    diff = C - expected_cont
    ratio = (n * dt) / C
    rows.append({
        'id': c['id'],
        'dt': dt,
        'n': n,
        'n*dt': n * dt,
        'C': C,
        'C*18.3': C * 18.3,
        'expected': expected_cont,
        'diff': diff,
        'ratio': ratio
    })

df = pd.DataFrame(rows)

print("Cases with LARGEST POSITIVE DIFF (C >> expected):")
print(df.sort_values(by='diff', ascending=False)[['id', 'dt', 'n', 'n*dt', 'C', 'C*18.3', 'expected', 'diff', 'ratio']].head(10).to_string(index=False))

print("\nCases with LARGEST NEGATIVE DIFF (C << expected):")
print(df.sort_values(by='diff', ascending=True)[['id', 'dt', 'n', 'n*dt', 'C', 'C*18.3', 'expected', 'diff', 'ratio']].head(10).to_string(index=False))
