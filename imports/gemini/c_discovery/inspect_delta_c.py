import json
import pandas as pd
from collections import Counter

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = master['cases']
long_cases = [c for c in cases if c['bars'] >= 21 and c.get('C_Lite') is not None]

diffs = []
for c in long_cases:
    n = c['bars']
    dt = c['dt']
    total_sec = n * dt
    c_val = round(c['C_Lite'])
    pred_base = round(total_sec * 10.0 / 183.0)
    delta_c = c_val - pred_base
    diffs.append((delta_c, c_val, pred_base, n, dt, c['id']))

counts = Counter([d[0] for d in diffs])
print("Distribution of Delta C = C - round(n * dt / 18.3):")
for delta, cnt in sorted(counts.items()):
    print(f"Delta C = {delta:3d} (mod 9 = {delta % 9}, mod 3 = {delta % 3}): count = {cnt}")

print("\nLet's check if Delta C are close to multiples of 9 or 27:")
for d in diffs[:20]:
    delta, c_val, pred_base, n, dt, cid = d
    print(f"{cid:35s} | dt={dt:2d} | n={n:3d} | C={c_val:3d} | Base={pred_base:3d} | Delta={delta:3d}")
