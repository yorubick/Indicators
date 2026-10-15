import csv, datetime
from pathlib import Path

ref_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(ref_path.open(encoding='utf-8-sig')))

candle_map = {}
for r in rows:
    candle_map[int(r['time'])] = r

def to_ts(time_str):
    return int(datetime.datetime.fromisoformat('2026-10-12T' + time_str + '+00:00').timestamp())

print("Candles around END (19:18:00 to 19:22:30):")
for t in range(to_ts('19:18:00'), to_ts('19:22:30') + 1, 15):
    if t in candle_map:
        r = candle_map[t]
        dt_str = datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime('%H:%M:%S')
        print(f"{dt_str} | O:{float(r['open']):8.2f} H:{float(r['high']):8.2f} L:{float(r['low']):8.2f} C:{float(r['close']):8.2f}")
