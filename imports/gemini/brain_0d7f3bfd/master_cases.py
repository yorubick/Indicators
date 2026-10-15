import csv, json, datetime
from pathlib import Path
import numpy as np

# Load reference 15s data
ref_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_path.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

# Also load 1m reference
ref_1m_path = Path('G:/trading/guias/analisis/character_manual_15m_1m.csv')
rows_1m = list(csv.DictReader(ref_1m_path.open(encoding='utf-8-sig')))
candles_1m = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_1m}

def ts(date_str, time_str):
    return int(datetime.datetime.fromisoformat(f"{date_str}T{time_str}+00:00").timestamp())

# Compile the table of known cases
cases = [
    # Morning 1m
    ('2026-10-12', '04:45:00', '04:50:00', 60, 60, candles_1m),
    ('2026-10-12', '04:45:00', '05:00:00', 60, 60, candles_1m),
    ('2026-10-12', '04:45:00', '05:05:00', 60, 75, candles_1m),
    ('2026-10-12', '04:45:00', '05:15:00', 60, 116, candles_1m),
    ('2026-10-12', '04:45:00', '05:25:00', 60, 113, candles_1m),
    ('2026-10-12', '04:45:00', '05:30:00', 60, 110, candles_1m),
    
    # Evening 1m
    ('2026-10-12', '18:50:00', '19:20:00', 60, 118, candles_1m),
    ('2026-10-12', '18:54:00', '19:20:00', 60, 134, candles_1m),
    ('2026-10-12', '18:55:00', '19:20:00', 60, 62, candles_1m),
    ('2026-10-12', '18:56:00', '19:20:00', 60, 109, candles_1m),
    ('2026-10-12', '18:57:00', '19:20:00', 60, 77, candles_1m),
    ('2026-10-12', '18:58:00', '19:20:00', 60, 77, candles_1m),
    ('2026-10-12', '18:59:00', '19:20:00', 60, 77, candles_1m),
    ('2026-10-12', '19:00:00', '19:20:00', 60, 77, candles_1m),
    ('2026-10-12', '19:11:00', '19:31:00', 60, 80, candles_1m),
    
    # Evening 15s START sweep (END 19:20:00)
    ('2026-10-12', '18:52:00', '19:20:00', 15, 67, candles_15s),
    ('2026-10-12', '18:53:00', '19:20:00', 15, 118, candles_15s),
    ('2026-10-12', '18:54:00', '19:20:00', 15, 123, candles_15s),
    ('2026-10-12', '18:54:15', '19:20:00', 15, 118, candles_15s),
    ('2026-10-12', '18:54:30', '19:20:00', 15, 67, candles_15s),
    ('2026-10-12', '18:54:45', '19:20:00', 15, 67, candles_15s),
    ('2026-10-12', '18:55:00', '19:20:00', 15, 106, candles_15s),
    ('2026-10-12', '18:55:15', '19:20:00', 15, 66, candles_15s),
    ('2026-10-12', '18:55:30', '19:20:00', 15, 88, candles_15s),
    ('2026-10-12', '18:55:45', '19:20:00', 15, 88, candles_15s),
    ('2026-10-12', '18:56:00', '19:20:00', 15, 106, candles_15s),
    ('2026-10-12', '18:56:15', '19:20:00', 15, 67, candles_15s),
    ('2026-10-12', '18:56:30', '19:20:00', 15, 67, candles_15s),
    ('2026-10-12', '18:56:45', '19:20:00', 15, 79, candles_15s),
    ('2026-10-12', '18:57:00', '19:20:00', 15, 67, candles_15s),
    ('2026-10-12', '19:01:00', '19:20:00', 15, 47, candles_15s),
    ('2026-10-12', '19:02:00', '19:20:00', 15, 47, candles_15s),
    
    # Evening 15s END sweep (START 18:55:00)
    ('2026-10-12', '18:55:00', '19:18:00', 15, 88, candles_15s),
    ('2026-10-12', '18:55:00', '19:19:00', 15, 115, candles_15s),
    ('2026-10-12', '18:55:00', '19:20:15', 15, 79, candles_15s),
    ('2026-10-12', '18:55:00', '19:20:30', 15, 67, candles_15s),
    ('2026-10-12', '18:55:00', '19:20:45', 15, 66, candles_15s),
    ('2026-10-12', '18:55:00', '19:21:00', 15, 115, candles_15s),
    ('2026-10-12', '18:55:00', '19:21:15', 15, 106, candles_15s),
    ('2026-10-12', '18:55:00', '19:21:30', 15, 79, candles_15s),
    ('2026-10-12', '18:55:00', '19:21:45', 15, 66, candles_15s),
    ('2026-10-12', '18:55:00', '19:22:00', 15, 106, candles_15s),
]

print(f"Loaded {len(cases)} test cases.")

# Let's extract properties for each case
dataset = []
for date, s, e, dt, C, c_map in cases:
    t_s = ts(date, s)
    t_e = ts(date, e)
    sub = [c_map[t] for t in range(t_s, t_e + 1, dt) if t in c_map]
    if not sub:
        continue
    highs = [x['high'] for x in sub]
    lows = [x['low'] for x in sub]
    closes = [x['close'] for x in sub]
    opens = [x['open'] for x in sub]
    
    dataset.append({
        's': s, 'e': e, 'dt': dt, 'C': C, 'bars': len(sub),
        'high': max(highs), 'low': min(lows), 'range': max(highs) - min(lows),
        'open': opens[0], 'close': closes[-1],
        'idx_max': highs.index(max(highs)),
        'idx_min': lows.index(min(lows)),
        'sub': sub
    })

print(f"Valid cases processed: {len(dataset)}")
