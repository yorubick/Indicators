"""Comprueba fuentes y reconstruye curvas exportadas, sin usar codigo privado."""
import csv
import json
import math
from pathlib import Path
import identificar_emas as fit

ROOT = Path(__file__).parent
with (ROOT / 'seven_cloud_1m.csv').open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))[:-1]
results = {}
for col, length in [('R4 E78', 78), ('R4 E84', 84)]:
    sources = {}
    for name, source in fit.SOURCES.items():
        alpha = 2/(length+1)
        errors = [float(r[col]) - (float(p[col]) + alpha*(source(r)-float(p[col])))
                  for p, r in zip(rows, rows[1:])
                  if p[col] and r[col] and int(r['time'])-int(p['time']) == 60]
        sources[name] = {'rmse': math.sqrt(sum(e*e for e in errors)/len(errors)),
                         'max_error': max(map(abs, errors)), 'pairs': len(errors)}
    results[col] = sources

with (ROOT/'character_manual_15m_1m.csv').open(encoding='utf-8-sig', newline='') as f:
    character = list(csv.DictReader(f))[:-1]
anchor = 1791781200  # 2026-10-12 05:00 UTC
anchor_row = next(r for r in character if int(r['time']) == anchor)
# La semilla inferida independientemente es 31254.25: coincide con HIGH,
# no con CLOSE. Esto esta comprobado para este anclaje, no para todo modo.
seed = float(anchor_row['high'])
periods = dict(zip(fit.COLUMNS, [24,30,8,10,3,3,72,89,216,267]))
state = dict.fromkeys(periods, seed)
errors = {k: [] for k in periods}
for r in character:
    if int(r['time']) <= anchor:
        continue
    for k, n in periods.items():
        state[k] += 2/(n+1)*(float(r['close'])-state[k])
        if r[k]:
            errors[k].append(state[k]-float(r[k]))
results['character_full_reconstruction'] = {
    'anchor_utc': '2026-10-12 05:00', 'seed_high': seed,
    'anchor_ohlc': {k: float(anchor_row[k]) for k in ['open','high','low','close']},
    'layers': {k: {'period': periods[k], 'points': len(e),
                    'max_error': max(map(abs,e)),
                    'rmse': math.sqrt(sum(x*x for x in e)/len(e))}
               for k,e in errors.items()}}
(ROOT/'verificacion_nubes.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
print(json.dumps(results, indent=2))
