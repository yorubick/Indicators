import csv, json, datetime
from pathlib import Path
import numpy as np

ref_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(ref_path.open(encoding='utf-8-sig')))

candle_map = {}
for r in rows:
    candle_map[int(r['time'])] = {
        'open': float(r['open']),
        'high': float(r['high']),
        'low': float(r['low']),
        'close': float(r['close']),
        'hl2': (float(r['high']) + float(r['low'])) / 2,
        'hlc3': (float(r['high']) + float(r['low']) + float(r['close'])) / 3,
        'ohlc4': (float(r['open']) + float(r['high']) + float(r['low']) + float(r['close'])) / 4,
    }

barrido = json.load(open('G:/trading/guias/analisis/C_barrido_ampliado.json', encoding='utf-8'))

def to_ts(time_str):
    return int(datetime.datetime.fromisoformat('2026-10-12T' + time_str + '+00:00').timestamp())

# Group cases by C
grouped_by_c = {}
for c in barrido['cases']:
    grouped_by_c.setdefault(c['C'], []).append(c['START_UTC'])

print("Grouped by C:")
for c_val, starts in sorted(grouped_by_c.items()):
    print(f"C = {c_val:3d} : {starts}")

# Let's inspect the candles at each start
print("\nCandles at START:")
for c in barrido['cases']:
    s = c['START_UTC']
    t = to_ts(s)
    cd = candle_map[t]
    print(f"START {s} (C={c['C']:3d}): O={cd['open']:.2f} H={cd['high']:.2f} L={cd['low']:.2f} C={cd['close']:.2f} | body={cd['close']-cd['open']:+.2f} range={cd['high']-cd['low']:.2f}")
