import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = [c for c in master['cases'] if c['bars'] >= 21 and c.get('C_Lite') is not None]
print(f"Total long Lite cases: {len(cases)}")

# We have files for each case or we can check the difference C - floor(n*dt/18.3)
# Let's inspect the distribution of delta = C - floor(n*dt/18.3)
diffs = []
for c in cases:
    n = c['bars']
    dt = c['dt']
    C = round(c['C_Lite'])
    baseline_floor = int(np.floor(n * dt / 18.3))
    baseline_round = int(round(n * dt / 18.3))
    diff_floor = C - baseline_floor
    diff_round = C - baseline_round
    diffs.append({
        'id': c['id'],
        'n': n,
        'dt': dt,
        'C': C,
        'floor': baseline_floor,
        'round': baseline_round,
        'diff_floor': diff_floor,
        'diff_round': diff_round
    })

df = pd.DataFrame(diffs)
print("\nDistribution of (C - floor) in Long Lite cases:")
print(df['diff_floor'].value_counts().sort_index())

print("\nDistribution of (C - round) in Long Lite cases:")
print(df['diff_round'].value_counts().sort_index())

# Check multiples of 3, 9, 27 in diff_floor
multiples_9 = (df['diff_floor'] % 9 == 0).sum()
print(f"\nExact multiples of 9 in (C - floor): {multiples_9} / {len(df)} ({multiples_9/len(df)*100:.1f}%)")
