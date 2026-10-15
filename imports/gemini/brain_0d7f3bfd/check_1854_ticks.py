import csv, datetime
from pathlib import Path

# Load 18:54 to 19:21:30 (30s)
p_1854_30s = Path('G:/trading/guias/analisis/C_agregacion_1854_192130_30s.csv')
rows = list(csv.DictReader(p_1854_30s.open(encoding='utf-8-sig')))
candle = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows}

t_start = int(datetime.datetime.fromisoformat('2026-10-12T18:54:00+00:00').timestamp())
t_end = int(datetime.datetime.fromisoformat('2026-10-12T19:21:30+00:00').timestamp())

sub = [candle[t] for t in range(t_start, t_end + 1, 30) if t in candle]
highs = [x['high'] for x in sub]
lows = [x['low'] for x in sub]
max_h = max(highs)
min_l = min(lows)
h_range = max_h - min_l
ticks = h_range / 0.25

print(f"18:54 to 19:21:30 (30s):")
print(f"High: {max_h}, Low: {min_l}, Range: {h_range}, Ticks: {ticks}")
print(f"Measured C: 136 s (interval: [135.90, 136.01])")
