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

# Define all confirmed cases
cases = [
    # 15s START sweep (END 19:20:00)
    ('15s START', '2026-10-12', '18:54:00', '19:20:00', 15, 123, candles_15s),
    ('15s START', '2026-10-12', '18:54:15', '19:20:00', 15, 118, candles_15s),
    ('15s START', '2026-10-12', '18:54:30', '19:20:00', 15, 67, candles_15s),
    ('15s START', '2026-10-12', '18:54:45', '19:20:00', 15, 67, candles_15s),
    ('15s START', '2026-10-12', '18:55:00', '19:20:00', 15, 106, candles_15s),
    ('15s START', '2026-10-12', '18:55:15', '19:20:00', 15, 66, candles_15s),
    ('15s START', '2026-10-12', '18:55:30', '19:20:00', 15, 88, candles_15s),
    ('15s START', '2026-10-12', '18:55:45', '19:20:00', 15, 88, candles_15s),
    ('15s START', '2026-10-12', '18:56:00', '19:20:00', 15, 106, candles_15s),
    ('15s START', '2026-10-12', '18:56:15', '19:20:00', 15, 67, candles_15s),
    ('15s START', '2026-10-12', '18:56:30', '19:20:00', 15, 67, candles_15s),
    ('15s START', '2026-10-12', '18:56:45', '19:20:00', 15, 79, candles_15s),
    ('15s START', '2026-10-12', '18:57:00', '19:20:00', 15, 67, candles_15s),
    
    # 15s END sweep (START 18:55:00)
    ('15s END', '2026-10-12', '18:55:00', '19:18:00', 15, 88, candles_15s),
    ('15s END', '2026-10-12', '18:55:00', '19:19:00', 15, 115, candles_15s),
    ('15s END', '2026-10-12', '18:55:00', '19:20:15', 15, 79, candles_15s),
    ('15s END', '2026-10-12', '18:55:00', '19:20:30', 15, 67, candles_15s),
    ('15s END', '2026-10-12', '18:55:00', '19:20:45', 15, 66, candles_15s),
    ('15s END', '2026-10-12', '18:55:00', '19:21:00', 15, 115, candles_15s),
    ('15s END', '2026-10-12', '18:55:00', '19:21:15', 15, 106, candles_15s),
    ('15s END', '2026-10-12', '18:55:00', '19:21:30', 15, 79, candles_15s),
    ('15s END', '2026-10-12', '18:55:00', '19:21:45', 15, 66, candles_15s),
    ('15s END', '2026-10-12', '18:55:00', '19:22:00', 15, 106, candles_15s),
    
    # 1m Morning (START 04:45:00)
    ('1m AM', '2026-10-12', '04:45:00', '04:50:00', 60, 60, candles_1m),
    ('1m AM', '2026-10-12', '04:45:00', '05:00:00', 60, 60, candles_1m),
    ('1m AM', '2026-10-12', '04:45:00', '05:05:00', 60, 75, candles_1m),
    ('1m AM', '2026-10-12', '04:45:00', '05:15:00', 60, 116, candles_1m),
    ('1m AM', '2026-10-12', '04:45:00', '05:25:00', 60, 113, candles_1m),
    ('1m AM', '2026-10-12', '04:45:00', '05:30:00', 60, 110, candles_1m),
    
    # 1m Evening (END 19:20:00)
    ('1m PM', '2026-10-12', '18:50:00', '19:20:00', 60, 118, candles_1m),
    ('1m PM', '2026-10-12', '18:54:00', '19:20:00', 60, 134, candles_1m),
    ('1m PM', '2026-10-12', '18:55:00', '19:20:00', 60, 62, candles_1m),
    ('1m PM', '2026-10-12', '18:56:00', '19:20:00', 60, 109, candles_1m),
    ('1m PM', '2026-10-12', '18:57:00', '19:20:00', 60, 77, candles_1m),
    ('1m PM', '2026-10-12', '18:58:00', '19:20:00', 60, 77, candles_1m),
    ('1m PM', '2026-10-12', '18:59:00', '19:20:00', 60, 77, candles_1m),
    ('1m PM', '2026-10-12', '19:00:00', '19:20:00', 60, 77, candles_1m),
    ('1m PM', '2026-10-12', '19:11:00', '19:31:00', 60, 80, candles_1m),
]

print(f"{'Group':<10} | {'Range':<15} | dt | {'C':>3} | {'C/89':>6} | {'C/72':>6} | {'C/dt':>5}")
print("-" * 65)

for grp, d, s, e, dt, C, c_map in cases:
    r89 = C / 89.0
    r72 = C / 72.0
    rdt = C / float(dt)
    print(f"{grp:<10} | {s[:5]}-{e[:5]:<8} | {dt:2d} | {C:3d} | {r89:6.3f} | {r72:6.3f} | {rdt:5.2f}")
