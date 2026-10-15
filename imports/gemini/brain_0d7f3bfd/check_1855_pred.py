# Let's inspect the candles between 18:55 and 19:20 on 12-Oct
import csv, datetime
from pathlib import Path

p = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

start_ts = ts('18:55:00')
end_ts = ts('19:20:00')

# Group 15s bars into 1m bars
sub_15 = [r for r in rows if start_ts <= int(r['time']) <= end_ts]
print(f"Total 15s rows between 18:55 and 19:20: {len(sub_15)}")

# Aggregate to 1m
bars_1m = []
for t in range(start_ts, end_ts + 60, 60):
    chunk = [r for r in rows if t <= int(r['time']) < t + 60]
    if chunk:
        bars_1m.append({
            'time': t,
            'open': float(chunk[0]['open']),
            'high': max(float(x['high']) for x in chunk),
            'low': min(float(x['low']) for x in chunk),
            'close': float(chunk[-1]['close'])
        })

print(f"Aggregated 1m bars: {len(bars_1m)}")
highs = [b['high'] for b in bars_1m]
lows = [b['low'] for b in bars_1m]
rng = max(highs) - min(lows)
print(f"18:55 to 19:20: Range = {rng}, High = {max(highs)}, Low = {min(lows)}, Open0 = {bars_1m[0]['open']}")

import evaluate_unified_model_v4 as ev
pred, branch = ev.predict_C({
    'bars': len(bars_1m),
    'dt': 60,
    'OHLC': bars_1m
})
print(f"Model v4 prediction for 18:55 to 19:20: C = {pred}, Branch = {branch}")
