import json
import pandas as pd

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = master['cases']

# Let's find all pairs of neighbor cases that differ by only 1 candle at START or END
pairs_start = []
pairs_end = []

case_dict = {}
for c in cases:
    if c.get('C_Lite') is not None and c['bars'] >= 21:
        case_dict[(c['dt'], c['START'], c['END'])] = c

for (dt, start, end), c1 in case_dict.items():
    # Check if there is another case with same START and different END
    # or same END and different START
    pass

# Let's collect all consecutive pairs in sweeps
# In 1m data:
# 1900_1920, 1900_1921, 1900_1922, 1900_1923, 1900_1924
ids_1m = [
    '20261012_190000_192000_60s',
    '20261012_190000_192100_60s',
    '20261012_190000_192200_60s',
    '20261012_190000_192300_60s',
    '20261012_190000_192400_60s',
]

print("1m END sweep (START 19:00:00):")
prev_c = None
for cid in ids_1m:
    c = next(x for x in cases if x['id'] == cid)
    c_val = round(c['C_Lite'])
    diff = c_val - prev_c if prev_c is not None else 0
    print(f"END: {c['END'].split('T')[1][:8]} | C: {c_val:3d} | diff: {diff:3d} (mod 3: {diff % 3}, mod 9: {diff % 9})")
    prev_c = c_val

# In 1m START sweep with fixed END 19:20:00:
start_sweep_1m = [
    ('18:54:00', 134),
    ('18:55:00', 62),
    ('18:56:00', 109),
    ('18:57:00', 77),
    ('18:58:00', 77),
    ('18:59:00', 77),
    ('19:00:00', 77)
]
print("\n1m START sweep (END 19:20:00):")
prev_c = None
for s, c_val in start_sweep_1m:
    diff = c_val - prev_c if prev_c is not None else 0
    print(f"START: {s} | C: {c_val:3d} | diff: {diff:3d} (mod 3: {diff % 3}, mod 9: {diff % 9})")
    prev_c = c_val
