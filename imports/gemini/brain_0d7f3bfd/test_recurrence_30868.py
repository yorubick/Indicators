import csv
from datetime import datetime, timezone
import numpy as np

with open('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

by_time = {int(r['time']): {k: float(r[k]) for k in ('open', 'high', 'low', 'close')} for r in rows}

def ts(t_str):
    return int(datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

# Target at 19:26:45:
# 3A: 30868.31, 3B: 30868.29
# 2A: 30868.49, 2B: 30868.43
# 1A: 30869.16, 1B: 30868.98

# Let's test different C values and seeds:
# In TV, is C = 62.0 s?
# If C = 62.0 s:
# What was the seed?
# Let's check what seed and what recurrence starts at what candle!
for t_seed_name, t_seed_str in [('19:23:30', '19:23:30'), ('19:23:45', '19:23:45'), ('19:20:00', '19:20:00')]:
    t_end = ts(t_seed_str)
    for seed_price in [
        by_time[t_end]['low'], 
        by_time[t_end]['high'], 
        by_time[t_end]['close'],
        by_time[t_end]['open'],
        30864.25, 30868.75, 30866.5, 30870.75, 30849.0,
        30868.0, 30868.25
    ]:
        for c_val in [62.0, 67.0, 61.0, 77.0, 88.0]:
            p3a = (72.0 / 3.0) * (c_val / 15.0)
            p3b = (89.0 / 3.0) * (c_val / 15.0)
            p2a = (72.0 / 9.0) * (c_val / 15.0)
            p2b = (89.0 / 9.0) * (c_val / 15.0)
            p1a = (72.0 / 27.0) * (c_val / 15.0)
            p1b = (89.0 / 27.0) * (c_val / 15.0)
            
            a3a, a3b = 2.0 / (p3a + 1.0), 2.0 / (p3b + 1.0)
            a2a, a2b = 2.0 / (p2a + 1.0), 2.0 / (p2b + 1.0)
            a1a, a1b = 2.0 / (p1a + 1.0), 2.0 / (p1b + 1.0)
            
            # Start recurrence from t_end + 15
            v3a = v3b = v2a = v2b = v1a = v1b = seed_price
            for t in range(t_end + 15, ts('19:26:45') + 15, 15):
                cl = by_time[t]['close']
                v3a += a3a * (cl - v3a)
                v3b += a3b * (cl - v3b)
                v2a += a2a * (cl - v2a)
                v2b += a2b * (cl - v2b)
                v1a += a1a * (cl - v1a)
                v1b += a1b * (cl - v1b)
            
            err = abs(v3a - 30868.31) + abs(v3b - 30868.29) + abs(v2a - 30868.49) + abs(v2b - 30868.43) + abs(v1a - 30869.16) + abs(v1b - 30868.98)
            if err < 0.15:
                print(f"HIT! t_end={t_seed_str}, seed={seed_price}, C={c_val}: total_err={err:.4f}")
                print(f"  3A: {v3a:.2f}, 3B: {v3b:.2f} | 2A: {v2a:.2f}, 2B: {v2b:.2f} | 1A: {v1a:.2f}, 1B: {v1b:.2f}")

