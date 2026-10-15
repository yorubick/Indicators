import json

with open('C:/Users/PC/.gemini/antigravity/brain/0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27/scratch/cases_112.json') as f:
    cases = json.load(f)

print('--- Cases with dt=15 and END ending in 19:20 ---')
for c in cases:
    if c['dt'] == 15 and '19:20' in c['END']:
        print(f"{c['START']} -> {c['END']}: C={c['C']}")

print('\n--- Cases with C == 88 ---')
for c in cases:
    if c.get('C') == 88:
        print(f"{c['START']} -> {c['END']} (dt={c['dt']}): C={c['C']}")
