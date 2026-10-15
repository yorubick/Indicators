import json
from collections import Counter

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = master['cases']

c_vals = []
for c in cases:
    if c['C_Lite'] is not None:
        c_vals.append((round(c['C_Lite']), c['dt'], c['bars'], c['id']))
    else:
        low = c['C_Character_interval']['lower_inclusive']
        high = c['C_Character_interval']['upper_exclusive']
        c_vals.append((round(low), c['dt'], c['bars'], c['id']))

# filter n >= 21
long_c = [x for x in c_vals if x[2] >= 21]
short_c = [x for x in c_vals if x[2] < 21]

print(f"Total long cases (n >= 21): {len(long_c)}")
counts_long = Counter([x[0] for x in long_c])
print("Distinct C values in long regime (sorted by frequency):")
for val, count in counts_long.most_common():
    print(f"  C = {val:3d}: count = {count:2d} (mod 9 = {val % 9}, mod 3 = {val % 3})")

print("\nAll unique C values in long regime (sorted numerically):")
sorted_unique = sorted(counts_long.keys())
print(sorted_unique)
diffs = [sorted_unique[i+1] - sorted_unique[i] for i in range(len(sorted_unique)-1)]
print("Differences between consecutive unique C values:")
print(diffs)
