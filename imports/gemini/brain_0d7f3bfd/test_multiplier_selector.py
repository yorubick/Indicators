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

print("Correlating target multipliers with structural price ratios:")

# Test various ratios:
# 1. Ratio of initial move to total range
# 2. Ratio of first swing height to range
# 3. Ratio of first candle body/range
# 4. Fib position of the start candle relative to total range
# 5. Fib position of the first swing high/low relative to total range

for s_str, C, target_m in start_cases:
    t_s = ts(s_str)
    sub = [candles_15s[t] for t in range(t_s, t_end + 15, 15) if t in candles_15s]
    h_tot = max(b['high'] for b in sub)
    l_tot = min(b['low'] for b in sub)
    rng_tot = h_tot - l_tot # 22.75 pts
    
    # Start candle position relative to range
    start_c = sub[0]['close']
    start_pos = (start_c - l_tot) / rng_tot # 0.0 to 1.0
    
    # First 4 bars high and low
    h_init = max(b['high'] for b in sub[:4])
    l_init = min(b['low'] for b in sub[:4])
    rng_init = h_init - l_init
    
    # Ratio of initial range to total range
    ratio_init = rng_init / rng_tot
    
    # Distance from start close to first swing extreme
    print(f"START {s_str} | C={C:3d} (m={target_m:.3f}) | start_pos={start_pos:.3f} | rng_init={rng_init:5.2f} (r={ratio_init:.3f})")
