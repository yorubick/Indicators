import csv, datetime
from pathlib import Path
import numpy as np

ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

start_cases = [
    ('18:54:00', 123),
    ('18:54:15', 118),
    ('18:54:30', 67),
    ('18:54:45', 67),
    ('18:55:00', 106),
    ('18:55:15', 66),
    ('18:55:30', 88),
    ('18:55:45', 88),
    ('18:56:00', 106),
    ('18:56:15', 67),
    ('18:56:30', 67),
    ('18:56:45', 79),
    ('18:57:00', 67),
]

t_end = ts('19:20:00')

# Let's track for each case:
# What is the highest high and lowest low of the first N bars (N=2, 3, 4, 5)?
for n in [2, 3, 4, 5, 6]:
    print(f"\n=== First {n} bars ===")
    for s_str, C in start_cases:
        t_s = ts(s_str)
        sub = [candles_15s[t] for t in range(t_s, t_end + 15, 15) if t in candles_15s][:n]
        h = max(b['high'] for b in sub)
        l = min(b['low'] for b in sub)
        diff = h - l
        # Check if C correlates with diff
        print(f"START {s_str} | C={C:3d} | H-L={diff:5.2f} pts ({diff/0.25:4.0f} ticks)")
