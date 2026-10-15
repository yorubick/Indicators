import json

with open(r'G:\trading\guias\analisis\resultado_C_meseta_1s_conteos.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for k in d:
    if k != 'records':
        print(k, ':', str(d[k])[:200])

print('rows count:', len(d.get('rows', [])))
for r in d.get('rows', []):
    print(f"n={r['n']}: C={r['C_Lite_reconstructed']:.4f}, pred={r.get('prediction_C')}, source={r.get('prediction_source')}, res={r.get('residual_C_minus_prediction')}")

