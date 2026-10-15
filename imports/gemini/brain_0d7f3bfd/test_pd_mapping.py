import csv, datetime
from pathlib import Path
import numpy as np

ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

# Test both START sweep and END sweep
all_cases_15s = [
    ('START', '18:54:00', '19:20:00', 123),
    ('START', '18:54:15', '19:20:00', 118),
    ('START', '18:54:30', '19:20:00', 67),
    ('START', '18:54:45', '19:20:00', 67),
    ('START', '18:55:00', '19:20:00', 106),
    ('START', '18:55:15', '19:20:00', 66),
    ('START', '18:55:30', '19:20:00', 88),
    ('START', '18:55:45', '19:20:00', 88),
    ('START', '18:56:00', '19:20:00', 106),
    ('START', '18:56:15', '19:20:00', 67),
    ('START', '18:56:30', '19:20:00', 67),
    ('START', '18:56:45', '19:20:00', 79),
    ('START', '18:57:00', '19:20:00', 67),
    ('END', '18:55:00', '19:18:00', 88),
    ('END', '18:55:00', '19:19:00', 115),
    ('END', '18:55:00', '19:20:00', 106),
    ('END', '18:55:00', '19:20:15', 79),
    ('END', '18:55:00', '19:20:30', 67),
    ('END', '18:55:00', '19:20:45', 66),
    ('END', '18:55:00', '19:21:00', 115),
    ('END', '18:55:00', '19:21:15', 106),
    ('END', '18:55:00', '19:21:30', 79),
    ('END', '18:55:00', '19:21:45', 66),
    ('END', '18:55:00', '19:22:00', 106),
]

print("Evaluating Premium / Discount mapping to C:")
for kind, s_str, e_str, C in all_cases_15s:
    t_s = ts(s_str)
    t_e = ts(e_str)
    sub = [candles_15s[t] for t in range(t_s, t_e + 15, 15) if t in candles_15s]
    h = max(b['high'] for b in sub)
    l = min(b['low'] for b in sub)
    rng = h - l
    
    # Equilibrium = 0.5 * (h + l)
    eq = 0.5 * (h + l)
    
    # End close relative to equilibrium
    c_end = sub[-1]['close']
    c_start = sub[0]['close']
    
    # Ratio relative to 89
    ratio = C / 89.0
    print(f"{kind:<5} {s_str}-{e_str} | C={C:3d} | ratio={ratio:5.3f} | Start_pos={(c_start-l)/rng:5.3f} | End_pos={(c_end-l)/rng:5.3f}")
