import csv, datetime
from pathlib import Path
import numpy as np

ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

start_cases = [
    ('18:54:00', 123, 1.382),
    ('18:54:15', 118, 1.333),
    ('18:54:30', 67,  0.750),
    ('18:54:45', 67,  0.750),
    ('18:55:00', 106, 1.191),
    ('18:55:15', 66,  0.750),
    ('18:55:30', 88,  1.000),
    ('18:55:45', 88,  1.000),
    ('18:56:00', 106, 1.191),
    ('18:56:15', 67,  0.750),
    ('18:56:30', 67,  0.750),
    ('18:56:45', 79,  0.889),
    ('18:57:00', 67,  0.750),
]

t_end = ts('19:20:00')

print("Examine properties of 13 START cases:")
print(f"{'START':<9} | {'C':>3} | {'Ratio':>5} | {'Sec':>3} | {'B0 C-O':>6} | {'B0 Dir':>6} | {'B0 Close':>8} | {'B0 High':>8} | {'B0 Low':>8}")
print("-" * 75)

for s_str, C, r in start_cases:
    t_s = ts(s_str)
    b0 = candles_15s[t_s]
    sec = int(s_str.split(':')[2])
    diff = b0['close'] - b0['open']
    b_dir = "BULL" if diff > 0 else ("BEAR" if diff < 0 else "DOJI")
    print(f"{s_str:<9} | {C:3d} | {r:5.3f} | {sec:3d} | {diff:6.2f} | {b_dir:>6} | {b0['close']:8.2f} | {b0['high']:8.2f} | {b0['low']:8.2f}")
