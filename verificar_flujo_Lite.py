"""Comprueba semillas y primera publicación de Lite; recibe C ya medido."""
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
LANES = ['Lane 3 A', 'Lane 3 B', 'Lane 2 A', 'Lane 2 B', 'Lane 1 A', 'Lane 1 B']
BASES = [72/3, 89/3, 72/9, 89/9, 72/27, 89/27]

def stamp(s):
    return int(datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp())

def check(path):
    info = json.loads(path.read_text(encoding='utf-8-sig'))
    with Path(info['file']).open(encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))[:-1]
    start, end = stamp(info['START_UTC']), stamp(info['END_UTC'])
    dt = info['chart_seconds']
    selected = [r for r in rows if start <= int(r['time']) <= end]
    bytime = {int(r['time']): r for r in rows}
    out = {'comparison': path.name}
    if any(t not in bytime for t in range(start, end + 1, dt)):
        return {**out, 'status': 'skipped_missing_range_OHLC'}
    high = max(float(r['high']) for r in selected)
    low = min(float(r['low']) for r in selected)
    post = [r for r in rows if end < int(r['time']) <= end + 5400]
    if any(t not in bytime for t in range(end + dt, end + 5401, dt)):
        return {**out, 'status': 'skipped_missing_post_END_OHLC'}
    breakout = next((r for r in post if float(r['close']) > high or float(r['close']) < low), None)
    if breakout is None:
        return {**out, 'status': 'skipped_no_break_within_90min'}
    bull = float(breakout['close']) > high
    seed = float(bytime[end]['low' if bull else 'high'])
    # Use the mean of six independently recovered C values, with no price fit.
    C = sum(info['Lite_C_assuming_unrounded_family'].values()) / 6
    periods = [base * C / dt for base in BASES]
    state = [seed] * 6
    errors = []
    violations = []
    first_plot = {}
    for r in post:
        t, close = int(r['time']), float(r['close'])
        state = [y + 2/(N+1)*(close-y) for y, N in zip(state, periods)]
        for lane, y in zip(LANES, state):
            visible = bool(r[lane])
            expected = t >= int(breakout['time'])
            if visible != expected:
                violations.append({'time':t, 'lane':lane, 'visible':visible})
            if visible:
                first_plot.setdefault(lane, t)
                errors.append(abs(float(r[lane])-y))
    return {**out, 'status':'checked', 'direction':'bull' if bull else 'bear',
            'C_measured':C, 'END_seed':seed, 'breakout_UTC':datetime.fromtimestamp(int(breakout['time']), timezone.utc).isoformat(),
            'first_plots':first_plot, 'compared_values':len(errors),
            'max_error':max(errors, default=None), 'visibility_violations':violations}

def main():
    results = [check(p) for p in sorted(ROOT.glob('Lite_*_comparacion.json'))]
    checked = [r for r in results if r['status']=='checked']
    out = {'scope':'C is supplied from Lite periods; this does not identify the OHLC generator of C.',
           'results':results, 'checked_cases':len(checked),
           'compared_values':sum(r['compared_values'] for r in checked),
           'max_error':max((r['max_error'] for r in checked if r['max_error'] is not None), default=None),
           'visibility_violations':sum(len(r['visibility_violations']) for r in checked)}
    (ROOT/'Lite_flujo_verificacion.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out, indent=2))

if __name__=='__main__':
    main()
