import csv
from datetime import datetime, timezone
import numpy as np
from scipy.optimize import minimize

with open('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

by_time = {int(r['time']): {k: float(r[k]) for k in ('open', 'high', 'low', 'close')} for r in rows}

def ts(t_str):
    return int(datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

target_vals = np.array([30868.31, 30868.29, 30868.49, 30868.43, 30869.16, 30868.98])
bases = np.array([72.0/3.0, 89.0/3.0, 72.0/9.0, 89.0/9.0, 72.0/27.0, 89.0/27.0])

for t_end_str in ['19:20:00', '19:21:00', '19:22:00', '19:23:00', '19:23:15', '19:23:30', '19:23:45']:
    t_end = ts(t_end_str)
    closes = [by_time[t]['close'] for t in range(t_end + 15, ts('19:26:45') + 15, 15) if t in by_time]
    
    # We want to find (seed, C)
    def loss(x):
        seed, c_val = x
        if c_val <= 1.0: return 1e6
        lens = bases * (c_val / 15.0)
        alphas = 2.0 / (lens + 1.0)
        v = np.full(6, seed)
        for cl in closes:
            v = v + alphas * (cl - v)
        return np.sum((v - target_vals)**2)
    
    # Try starting from various seeds
    for s0 in [30868.25, 30866.0, 30864.25, 30870.75]:
        for c0 in [62.0, 67.0]:
            res = minimize(loss, [s0, c0], method='Nelder-Mead')
            if res.fun < 1e-4:
                seed_opt, c_opt = res.x
                lens = bases * (c_opt / 15.0)
                alphas = 2.0 / (lens + 1.0)
                v = np.full(6, seed_opt)
                for cl in closes: v = v + alphas * (cl - v)
                print(f"EXACT MATCH FOUND! END={t_end_str}: Seed={seed_opt:.4f}, C={c_opt:.2f} s")
                print(f"  Result: {np.round(v, 2)}")
                print(f"  Target: {target_vals}")
                print(f"  Residual: {res.fun:.6e}\n")
                break
        else:
            continue
        break
