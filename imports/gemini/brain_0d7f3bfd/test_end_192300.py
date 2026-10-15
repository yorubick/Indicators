import csv
from datetime import datetime, timezone
import numpy as np

with open('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

by_time = {int(r['time']): {k: float(r[k]) for k in ('open', 'high', 'low', 'close')} for r in rows}

def ts(t_str):
    return int(datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

t_end = ts('19:23:00')
t_target = ts('19:26:45')
seed = 30868.25 # Low of 19:23:00 bar

bases = [72.0/3.0, 89.0/3.0, 72.0/9.0, 89.0/9.0, 72.0/27.0, 89.0/27.0]

for c_val in [66.83, 67.0]:
    v = [seed] * 6
    alphas = [2.0 / (b * (c_val / 15.0) + 1.0) for b in bases]
    for t in range(t_end + 15, t_target + 15, 15):
        cl = by_time[t]['close']
        for i in range(6):
            v[i] += alphas[i] * (cl - v[i])
    print(f"C={c_val}:")
    print(f"  Lane 3 A/B: {v[0]:.2f} / {v[1]:.2f}")
    print(f"  Lane 2 A/B: {v[2]:.2f} / {v[3]:.2f}")
    print(f"  Lane 1 A/B: {v[4]:.2f} / {v[5]:.2f}")
