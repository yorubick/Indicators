import csv, datetime
from pathlib import Path
import numpy as np

# Load morning cases
ref_1m_path = Path('G:/trading/guias/analisis/manual/Lite_0445_051500_1m_a.csv')
rows_1m = list(csv.DictReader(ref_1m_path.open(encoding='utf-8-sig')))
candles_1m = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_1m}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

morning_cases = [
    ('04:50:00', 6, 60),
    ('05:00:00', 16, 60),
    ('05:05:00', 21, 75),
    ('05:15:00', 31, 116),
    ('05:25:00', 41, 113),
    ('05:30:00', 46, 110),
]

t_start = ts('04:45:00')

print("Morning cases analysis:")
for e_str, n_expected, C in morning_cases:
    t_end = ts(e_str)
    sub = [candles_1m[t] for t in range(t_start, t_end + 60, 60) if t in candles_1m]
    h = max(b['high'] for b in sub)
    l = min(b['low'] for b in sub)
    rng = h - l
    n = len(sub)
    
    # Velocity: points per bar
    v = rng / n
    # Inverse: bars per point
    inv_v = n / rng
    
    # Ticks per bar
    ticks_per_bar = (rng / 0.25) / n
    
    print(f"04:45 to {e_str[:5]} | bars={n:2d} | C={C:3d} | Rng={rng:5.2f} | Rng/bars={v:.4f} | bars/Rng={inv_v:.4f} | ticks/bar={ticks_per_bar:.4f}")
