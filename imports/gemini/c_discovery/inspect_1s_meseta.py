import json

with open(r'G:\trading\guias\analisis\resultado_C_meseta_1s_conteos.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"Total rows: {len(d['rows'])}")
for r in d['rows']:
    c_val = r['C_Lite_reconstructed']
    pred = r.get('prediction_C')
    print(f"n={r['n']:2d} | END={r['END_UTC']} | C={c_val:.6f} | pred={pred} | new_H={r.get('new_high')} | new_L={r.get('new_low')}")
