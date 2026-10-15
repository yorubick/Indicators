import json

with open('C:/Users/PC/.gemini/antigravity/brain/0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27/scratch/cases_112.json') as f:
    cases = json.load(f)

for c in cases:
    if '19:20' in c['END'] or '19:23' in c['END']:
        print(f"{c['START']} -> {c['END']} (dt={c['dt']}): C={c['C']}")
