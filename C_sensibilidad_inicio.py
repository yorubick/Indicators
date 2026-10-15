"""Controles de START con END fijo. Recupera C; no lo predice desde OHLC."""
import csv
import json
from pathlib import Path
from datetime import datetime, timezone
from obtener_C import recover

ROOT = Path(__file__).parent
CASES = [
    ('C_end1920_start1850_chart.csv', '18:50'),
    ('C_end1920_start1854_chart.csv', '18:54'),
    ('C_25m_live_confirmado.csv', '18:55'),
    ('C_end1920_start1856_chart.csv', '18:56'),
    ('C_end1920_start1857_chart.csv', '18:57'),
    ('C_end1920_start1858_chart.csv', '18:58'),
    ('C_end1920_start1859_chart.csv', '18:59'),
    ('C_end1920_start1900_chart.csv', '19:00'),
    ('C_start1854_repetido.csv', '18:54'),
]

def stamp(time):
    return int(datetime.fromisoformat('2026-10-12T' + time + ':00+00:00').timestamp())

def main():
    results = []
    for file, start in CASES:
        path = ROOT / file
        extracted = recover(path)
        rows = list(csv.DictReader(path.open(encoding='utf-8-sig', newline='')))
        segment = [r for r in rows if stamp(start) <= int(r['time']) <= stamp('19:20')]
        assert int(segment[0]['time']) == stamp(start)
        assert int(segment[-1]['time']) == stamp('19:20')
        record = {
            'file': file, 'START_UTC': start, 'END_UTC': '19:20',
            'duration_minutes': (stamp('19:20') - stamp(start)) // 60,
            'range_high': max(float(r['high']) for r in segment),
            'range_low': min(float(r['low']) for r in segment),
            'start_OHLC': {k: float(segment[0][k]) for k in ['open', 'high', 'low', 'close']},
            'end_OHLC': {k: float(segment[-1][k]) for k in ['open', 'high', 'low', 'close']},
            'extraction': extracted,
        }
        results.append(record)
        print(start, extracted['compatible_integer_C_seconds'], record['range_high'], record['range_low'])

    first, repeat = results[1], results[-1]
    assert first['extraction']['periods'] == repeat['extraction']['periods']
    assert first['extraction']['C_seconds_interval'] == repeat['extraction']['C_seconds_interval']
    # Historical OHLC over the identical common window must remain unchanged.
    reference = None
    for file, start in CASES:
        rows = list(csv.DictReader((ROOT / file).open(encoding='utf-8-sig')))
        common = [(int(r['time']), *(float(r[k]) for k in ['open','high','low','close']))
                  for r in rows if stamp('19:00') <= int(r['time']) <= stamp('19:20')]
        if reference is None:
            reference = common
        assert reference == common, file
    output = {'date_UTC': '2026-10-12', 'source_seconds': 60, 'profile': 'B',
              'mode': 'Manual', 'common_OHLC_identical': True, 'cases': results,
              'scope': 'C extraido de plots; no es una formula generadora de C.'}
    (ROOT / 'C_sensibilidad_inicio.json').write_text(json.dumps(output, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
