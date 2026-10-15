import json

with open(r'G:\trading\guias\analisis\Gemini_v31_auditoria.json') as f:
    aud = json.load(f)

print("Keys in aud:", list(aud.keys()))
for k in aud:
    if 'additional' in k:
        print(f"Key {k}: {len(aud[k])} items")
        for item in aud[k]:
            print(f"  ID: {item.get('id')} | dt={item.get('dt')} | bars={item.get('bars')} | actual_C={item.get('C')} | pred={item.get('pred')} | err={item.get('error')}")
