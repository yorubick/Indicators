import json

with open(r'G:\trading\guias\analisis\Gemini_v31_auditoria.json') as f:
    aud = json.load(f)

rows = aud.get('rows', [])
print(f"Total rows in audit: {len(rows)}")

add_rows = [r for r in rows if r.get('split') in ['additional_controls', 'additional15s'] or 'additional' in str(r.get('split'))]
if not add_rows:
    # check if there's any other field
    add_rows = [r for r in rows if r.get('dt') == 15 and r.get('bars') >= 21]

print(f"Additional or long 15s rows: {len(add_rows)}")
for r in add_rows[:20]:
    print(f"ID: {r.get('id')} | dt={r.get('dt')} | bars={r.get('bars')} | actual_C={r.get('C')} | pred={r.get('pred')} | split={r.get('split')}")
