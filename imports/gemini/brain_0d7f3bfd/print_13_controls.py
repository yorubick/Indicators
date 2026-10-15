import json

with open(r'G:\trading\guias\analisis\Gemini_v31_auditoria.json') as f:
    aud = json.load(f)

rows = aud.get('rows', [])
for i in range(99, len(rows)):
    r = rows[i]
    print(f"Index {i}: ID={r.get('id')} | dt={r.get('dt')} | bars={r.get('bars')} | C={r.get('C')} | START={r.get('START')} | END={r.get('END')}")
