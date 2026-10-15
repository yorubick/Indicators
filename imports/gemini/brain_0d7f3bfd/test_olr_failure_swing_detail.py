import csv, datetime
from pathlib import Path
import numpy as np

p = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

c_map = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows}

end_cases = [
    ('19:18:00', 88),
    ('19:19:00', 115),
    ('19:20:00', 106),
    ('19:20:15', 79),
    ('19:20:30', 67),
    ('19:20:45', 66),
    ('19:21:00', 115),
    ('19:21:15', 106),
    ('19:21:30', 79),
    ('19:21:45', 66),
    ('19:22:00', 106),
]

start_ts = ts('18:55:00')

print("=== Analyzing END sweep bars from 19:18 to 19:22 ===")
for end_str, C in end_cases:
    end_ts = ts(end_str)
    sub = [c_map[t] for t in range(start_ts, end_ts + 15, 15) if t in c_map]
    n_bars = len(sub)
    
    # Let's inspect the last 10 bars before END
    recent = sub[-10:]
    recent_highs = [b['high'] for b in recent]
    recent_lows = [b['low'] for b in recent]
    
    # Distance in seconds from the most recent local pivot high/low
    # Pivot high: high > high[1] and high > high[-1]
    pivots_h = []
    for i in range(1, len(sub)-1):
        if sub[i]['high'] >= sub[i-1]['high'] and sub[i]['high'] >= sub[i+1]['high']:
            pivots_h.append((i, sub[i]['high']))
            
    pivots_l = []
    for i in range(1, len(sub)-1):
        if sub[i]['low'] <= sub[i-1]['low'] and sub[i]['low'] <= sub[i+1]['low']:
            pivots_l.append((i, sub[i]['low']))
            
    last_ph = pivots_h[-1] if pivots_h else (0, 0)
    last_pl = pivots_l[-1] if pivots_l else (0, 0)
    
    dist_ph = (n_bars - 1 - last_ph[0]) * 15
    dist_pl = (n_bars - 1 - last_pl[0]) * 15
    
    print(f"END {end_str} | C={C:3d} | Bars={n_bars:3d} | Last PH bar={last_ph[0]:2d} (t-{dist_ph:3d}s) | Last PL bar={last_pl[0]:2d} (t-{dist_pl:3d}s)")
