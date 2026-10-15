import csv, datetime, math
from pathlib import Path
import numpy as np

# Load datasets
ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

ref_1m_path = Path('G:/trading/guias/analisis/manual/Lite_0445_051500_1m_a.csv')
rows_1m = list(csv.DictReader(ref_1m_path.open(encoding='utf-8-sig')))
candles_1m = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_1m}

def ts(d_str, t_str):
    return int(datetime.datetime.fromisoformat(f"{d_str}T{t_str}+00:00").timestamp())

# Confirmed cases
cases = [
    # 15s START sweep (END 19:20:00)
    ('15s', '2026-10-12', '18:54:00', '19:20:00', 15, 123, candles_15s),
    ('15s', '2026-10-12', '18:54:15', '19:20:00', 15, 118, candles_15s),
    ('15s', '2026-10-12', '18:54:30', '19:20:00', 15, 67, candles_15s),
    ('15s', '2026-10-12', '18:54:45', '19:20:00', 15, 67, candles_15s),
    ('15s', '2026-10-12', '18:55:00', '19:20:00', 15, 106, candles_15s),
    ('15s', '2026-10-12', '18:55:15', '19:20:00', 15, 66, candles_15s),
    ('15s', '2026-10-12', '18:55:30', '19:20:00', 15, 88, candles_15s),
    ('15s', '2026-10-12', '18:55:45', '19:20:00', 15, 88, candles_15s),
    ('15s', '2026-10-12', '18:56:00', '19:20:00', 15, 106, candles_15s),
    ('15s', '2026-10-12', '18:56:15', '19:20:00', 15, 67, candles_15s),
    ('15s', '2026-10-12', '18:56:30', '19:20:00', 15, 67, candles_15s),
    ('15s', '2026-10-12', '18:56:45', '19:20:00', 15, 79, candles_15s),
    ('15s', '2026-10-12', '18:57:00', '19:20:00', 15, 67, candles_15s),
    
    # 15s END sweep (START 18:55:00)
    ('15s', '2026-10-12', '18:55:00', '19:18:00', 15, 88, candles_15s),
    ('15s', '2026-10-12', '18:55:00', '19:19:00', 15, 115, candles_15s),
    ('15s', '2026-10-12', '18:55:00', '19:20:15', 15, 79, candles_15s),
    ('15s', '2026-10-12', '18:55:00', '19:20:30', 15, 67, candles_15s),
    ('15s', '2026-10-12', '18:55:00', '19:20:45', 15, 66, candles_15s),
    ('15s', '2026-10-12', '18:55:00', '19:21:00', 15, 115, candles_15s),
    ('15s', '2026-10-12', '18:55:00', '19:21:15', 15, 106, candles_15s),
    ('15s', '2026-10-12', '18:55:00', '19:21:30', 15, 79, candles_15s),
    ('15s', '2026-10-12', '18:55:00', '19:21:45', 15, 66, candles_15s),
    ('15s', '2026-10-12', '18:55:00', '19:22:00', 15, 106, candles_15s),
    
    # 1m Morning (START 04:45:00)
    ('1m', '2026-10-12', '04:45:00', '04:50:00', 60, 60, candles_1m),
    ('1m', '2026-10-12', '04:45:00', '05:00:00', 60, 60, candles_1m),
    ('1m', '2026-10-12', '04:45:00', '05:05:00', 60, 75, candles_1m),
    ('1m', '2026-10-12', '04:45:00', '05:15:00', 60, 116, candles_1m),
    ('1m', '2026-10-12', '04:45:00', '05:25:00', 60, 113, candles_1m),
    ('1m', '2026-10-12', '04:45:00', '05:30:00', 60, 110, candles_1m),
    
    # 1m Evening (END 19:20:00)
    ('1m', '2026-10-12', '18:50:00', '19:20:00', 60, 118, candles_1m),
    ('1m', '2026-10-12', '18:54:00', '19:20:00', 60, 134, candles_1m),
    ('1m', '2026-10-12', '18:55:00', '19:20:00', 60, 62, candles_1m),
    ('1m', '2026-10-12', '18:56:00', '19:20:00', 60, 109, candles_1m),
    ('1m', '2026-10-12', '18:57:00', '19:20:00', 60, 77, candles_1m),
    ('1m', '2026-10-12', '18:58:00', '19:20:00', 60, 77, candles_1m),
    ('1m', '2026-10-12', '18:59:00', '19:20:00', 60, 77, candles_1m),
    ('1m', '2026-10-12', '19:00:00', '19:20:00', 60, 77, candles_1m),
    ('1m', '2026-10-12', '19:11:00', '19:31:00', 60, 80, candles_1m),
]

data = []
for grp, d, s, e, dt, C, c_map in cases:
    t_s = ts(d, s)
    t_e = ts(d, e)
    sub = [c_map[t] for t in range(t_s, t_e + dt, dt) if t in c_map]
    if len(sub) < 2:
        continue
    highs = [x['high'] for x in sub]
    lows = [x['low'] for x in sub]
    closes = [x['close'] for x in sub]
    opens = [x['open'] for x in sub]
    
    data.append({
        'name': f"{s[:5]}-{e[:5]} ({dt}s)",
        'grp': grp, 'dt': dt, 'C': C, 'sub': sub,
        'highs': highs, 'lows': lows, 'closes': closes, 'opens': opens,
        'H': max(highs), 'L': min(lows), 'range': max(highs) - min(lows),
        'n': len(sub), 'dur': len(sub) * dt
    })

print(f"Loaded {len(data)} cases.")

# Test: What if C is chosen from candidate set based on nearest match to a continuous metric?
# Let's test candidate continuous metrics:
# Metric 1: ATR-based duration
# Metric 2: Range / Velocity
# Metric 3: Fibonacci level of the close relative to range
candidate_c_grid = [15, 60, 62, 66, 67, 75, 77, 79, 80, 88, 106, 109, 110, 113, 115, 116, 118, 123, 134]

print(f"Grid size: {len(candidate_c_grid)} discrete values")
