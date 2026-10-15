import json

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

cases = data['cases']
splits = {}
for c in cases:
    splits.setdefault(c['split'], []).append(c)

for s, items in splits.items():
    short = [x for x in items if x['bars'] < 21]
    long_cases = [x for x in items if x['bars'] >= 21]
    print(f'Split {s}: total={len(items)}, short={len(short)}, long={len(long_cases)}')

print('\n--- Long cases in TRAINING (32 cases) ---')
for c in sorted([x for x in splits['training'] if x['bars'] >= 21], key=lambda x: (x['START'], x['bars'])):
    print(f"{c['START'][:19]} -> {c['END'][11:19]} | bars={c['bars']:2d} | dt={c['dt']:2d} | C={c['C']}")

print('\n--- Long cases in VALIDATION (27 cases) ---')
for c in sorted([x for x in splits['validation'] if x['bars'] >= 21], key=lambda x: (x['START'], x['bars'])):
    print(f"{c['START'][:19]} -> {c['END'][11:19]} | bars={c['bars']:2d} | dt={c['dt']:2d} | C={c['C']}")
