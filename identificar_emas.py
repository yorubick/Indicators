"""Ajusta la recurrencia EMA a plots exportados; omite la ultima vela en curso."""
import csv
import json
import math
from pathlib import Path
import sys

COLUMNS = ['Layer A', 'Layer A boundary', 'Layer B', 'Layer B boundary',
           'Layer C', 'Layer C boundary', 'Extra cloud 1', 'Extra cloud 1 boundary',
           'Extra cloud 2', 'Extra cloud 2 boundary']
SOURCES = {
    'close': lambda r: float(r['close']),
    'high': lambda r: float(r['high']),
    'low': lambda r: float(r['low']),
    'hl2': lambda r: (float(r['high']) + float(r['low'])) / 2,
    'ohlc4': lambda r: sum(float(r[k]) for k in ['open', 'high', 'low', 'close']) / 4,
}


def analyze(path, step_seconds=60):
    with path.open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))[:-1]
    output = {'file': str(path), 'rows_closed': len(rows), 'step_seconds': step_seconds, 'layers': {}}
    for column in COLUMNS:
        candidates = []
        for name, source in SOURCES.items():
            pairs = [(source(r) - float(prev[column]), float(r[column]) - float(prev[column]))
                     for prev, r in zip(rows, rows[1:]) if prev[column] and r[column]
                     and int(r['time']) - int(prev['time']) == step_seconds]
            denom = sum(x*x for x, y in pairs)
            if not pairs or not denom:
                continue
            alpha = sum(x*y for x, y in pairs) / denom
            errors = [y - alpha*x for x, y in pairs]
            candidates.append({'source': name, 'alpha': alpha, 'period': 2/alpha-1,
                               'rmse_step': math.sqrt(sum(e*e for e in errors)/len(errors)),
                               'max_error_step': max(abs(e) for e in errors), 'pairs': len(pairs)})
        if not candidates:
            output['layers'][column] = {'available': False, 'reason': 'No usable consecutive plotted values'}
            continue
        best = min(candidates, key=lambda item: item['rmse_step'])
        first = next(r for r in rows if r[column])
        source = SOURCES[best['source']]
        best['first_time'] = int(first['time'])
        best['implied_seed'] = (float(first[column]) - best['alpha'] * source(first)) / (1-best['alpha'])
        best['alternatives'] = sorted(candidates, key=lambda item: item['rmse_step'])[1:]
        output['layers'][column] = best
    return output


if __name__ == '__main__':
    results = [analyze(Path(p)) for p in sys.argv[1:]]
    destination = Path(__file__).with_name('ajuste_emas.json')
    destination.write_text(json.dumps(results, indent=2), encoding='utf-8')
    for result in results:
        print(Path(result['file']).name, result['rows_closed'], 'velas cerradas')
        for name, layer in result['layers'].items():
            if layer.get('available') is False:
                print(f"  {name}: {layer['reason']}")
                continue
            print(f"  {name}: {layer['source']} N={layer['period']:.9f}, RMSE={layer['rmse_step']:.3g}, seed={layer['implied_seed']:.8f}")
