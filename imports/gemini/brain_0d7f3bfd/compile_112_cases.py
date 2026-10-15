import json
from pathlib import Path

ROOT = Path(r"G:\trading\guias\analisis")

# 1. Master 93 cases
master = json.loads((ROOT / 'C_dataset_verificado.json').read_text(encoding='utf-8'))['cases']
cases_112 = [dict(c, partition=c['split']) for c in master]

# 2. Oct 13 6 cases
pred13 = json.loads((ROOT / 'C_evolucion87_predicciones.json').read_text(encoding='utf-8'))
res13 = json.loads((ROOT / 'C_evolucion87_resultados.json').read_text(encoding='utf-8'))
for c in res13['cases']:
    cases_112.append({
        'id': f'oct13_{c["END"][11:16]}',
        'START': '2026-10-13T06:25:00+00:00',
        'END': c['END'],
        'bars': c['bars'],
        'dt': 60,
        'C': c['C'],
        'OHLC': pred13['OHLC'][:c['bars']],
        'partition': 'oct13_existing'
    })

# 3. 13 Additional Controls
for tag in ['replica24', 'rama24_resolucion', 'transicion1923', 'prefijo192345', 'recorte1903']:
    preds = json.loads((ROOT / f'C_{tag}_predicciones.json').read_text(encoding='utf-8'))['cases']
    results = json.loads((ROOT / f'C_{tag}_resultados.json').read_text(encoding='utf-8'))['cases']
    by_id = {c['id']: c for c in preds}
    for r in results:
        c = by_id[r['id']]
        cases_112.append({
            'id': c['id'],
            'START': c['START'],
            'END': c['END'],
            'bars': c.get('bars', len(c['OHLC'])),
            'dt': c.get('dt', 60),
            'C': r['C'],
            'OHLC': c['OHLC'],
            'partition': 'additional_controls'
        })

print(f"Total compiled cases: {len(cases_112)}")

# Save to scratch for easy access
with open(r'C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\cases_112.json', 'w', encoding='utf-8') as f:
    json.dump(cases_112, f, indent=2)
print("Saved cases_112.json successfully.")
