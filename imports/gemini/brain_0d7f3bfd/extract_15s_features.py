import csv
from pathlib import Path
from datetime import datetime, timezone

# Load all 15s data
ref_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_path.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

def ts(s_str):
    return int(datetime.fromisoformat(f"2026-10-12T{s_str}+00:00").timestamp())

# Master cases for 15s
cases_15s = [
    # START sweep (END 19:20:00)
    ('18:52:00', '19:20:00', 67),
    ('18:53:00', '19:20:00', 118),
    ('18:54:00', '19:20:00', 123),
    ('18:54:15', '19:20:00', 118),
    ('18:54:30', '19:20:00', 67),
    ('18:54:45', '19:20:00', 67),
    ('18:55:00', '19:20:00', 106),
    ('18:55:15', '19:20:00', 66),
    ('18:55:30', '19:20:00', 88),
    ('18:55:45', '19:20:00', 88),
    ('18:56:00', '19:20:00', 106),
    ('18:56:15', '19:20:00', 67),
    ('18:56:30', '19:20:00', 67),
    ('18:56:45', '19:20:00', 79),
    ('18:57:00', '19:20:00', 67),
    ('19:01:00', '19:20:00', 47),
    ('19:02:00', '19:20:00', 47),
    
    # END sweep (START 18:55:00)
    ('18:55:00', '19:18:00', 88),
    ('18:55:00', '19:19:00', 115),
    ('18:55:00', '19:20:15', 79),
    ('18:55:00', '19:20:30', 67),
    ('18:55:00', '19:20:45', 66),
    ('18:55:00', '19:21:00', 115),
    ('18:55:00', '19:21:15', 106),
    ('18:55:00', '19:21:30', 79),
    ('18:55:00', '19:21:45', 66),
    ('18:55:00', '19:22:00', 106),
]

print("=== 15s CASES FEATURE EXTRACTION ===")
print(f"{'START':<9} {'END':<9} {'C':<5} {'Bars':<5} {'Range':<7} {'H_age':<6} {'L_age':<6} {'LastC':<9} {'EndSec':<6}")
for s, e, C in cases_15s:
    t_s, t_e = ts(s), ts(e)
    sub = [candles_15s[t] for t in range(t_s, t_e + 1, 15) if t in candles_15s]
    if not sub: continue
    highs = [x['high'] for x in sub]
    lows = [x['low'] for x in sub]
    max_h = max(highs)
    min_l = min(lows)
    h_idx = len(highs) - 1 - highs[::-1].index(max_h) # last index of max
    l_idx = len(lows) - 1 - lows[::-1].index(min_l)
    h_age = len(sub) - 1 - h_idx
    l_age = len(sub) - 1 - l_idx
    end_sec = e[6:8]
    print(f"{s:<9} {e:<9} {C:<5d} {len(sub):<5d} {max_h - min_l:<7.2f} {h_age:<6d} {l_age:<6d} {sub[-1]['close']:<9.2f} {end_sec:<6}")
