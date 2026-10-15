import csv, datetime
from pathlib import Path

path_30s = Path('G:/trading/guias/analisis/C_agregacion_1800_192130_30s.csv')
rows_30s = list(csv.DictReader(path_30s.open(encoding='utf-8-sig')))

candle_30s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_30s}

# Range: 18:00:00 to 19:21:30
# C = 196 seconds!
# What is 196 seconds in 30s bars? 196 / 30 = 6.53 bars.
# What is 196 seconds in 60s bars? 196 / 60 = 3.26 bars.
print(f"Total 30s rows: {len(rows_30s)}")
t_start = int(datetime.datetime.fromisoformat('2026-10-12T18:00:00+00:00').timestamp())
t_end = int(datetime.datetime.fromisoformat('2026-10-12T19:21:30+00:00').timestamp())

sub_30s = [candle_30s[t] for t in range(t_start, t_end + 1, 30) if t in candle_30s]
print(f"Sub 30s bars in range: {len(sub_30s)}")
highs = [x['high'] for x in sub_30s]
lows = [x['low'] for x in sub_30s]
max_h = max(highs)
min_l = min(lows)
print(f"Global High: {max_h} at index {highs.index(max_h)}")
print(f"Global Low:  {min_l} at index {lows.index(min_l)}")

# Let's check when max_h and min_l occurred:
t_max_h = t_start + highs.index(max_h) * 30
t_min_l = t_start + lows.index(min_l) * 30
print(f"Max H time: {datetime.datetime.fromtimestamp(t_max_h, datetime.timezone.utc)}")
print(f"Min L time: {datetime.datetime.fromtimestamp(t_min_l, datetime.timezone.utc)}")

# Let's check distance from end:
print(f"End time: {datetime.datetime.fromtimestamp(t_end, datetime.timezone.utc)}")
print(f"Distance from max_h to end: {t_end - t_max_h} s")
print(f"Distance from min_l to end: {t_end - t_min_l} s")
