import csv
from datetime import datetime, timezone
import numpy as np

# Load 15s data
with open('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

by_time = {int(r['time']): {k: float(r[k]) for k in ('open', 'high', 'low', 'close')} for r in rows}

def ts(t_str):
    return int(datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

# What if the chart is 15s vs 1m?
# In Pine Script Lab v4:
# If C = 62.0, what are the alpha values?
# p_lite_l3a = (72.0 / 3.0) * (C / dt) = 24 * (62 / dt)
# Let's test dt = 15, dt = 60, dt = 1
for dt in [15, 60]:
    c_final = 62.0
    p_lite_l3a = (72.0 / 3.0)  * (c_final / dt)
    p_lite_l3b = (89.0 / 3.0)  * (c_final / dt)
    p_lite_l2a = (72.0 / 9.0)  * (c_final / dt)
    p_lite_l2b = (89.0 / 9.0)  * (c_final / dt)
    p_lite_l1a = (72.0 / 27.0) * (c_final / dt)
    p_lite_l1b = (89.0 / 27.0) * (c_final / dt)
    
    calc_alpha = lambda len_: 2.0 / (len_ + 1.0)
    a_l3a, a_l3b = calc_alpha(p_lite_l3a), calc_alpha(p_lite_l3b)
    a_l2a, a_l2b = calc_alpha(p_lite_l2a), calc_alpha(p_lite_l2b)
    a_l1a, a_l1b = calc_alpha(p_lite_l1a), calc_alpha(p_lite_l1b)
    
    # In Lab v4:
    # is_end_bar is true when time == end_time
    # What was end_time? 19:23:30 (or what if user had end_time in input?)
    for end_str in ['19:23:30', '19:23:00', '19:20:00']:
        t_end = ts(end_str)
        if t_end not in by_time: continue
        end_bar = by_time[t_end]
        
        # In Lab v4:
        # s_bull := end_low
        # But wait! What if breakout_dir == "bull"?
        # breakout_dir is "bull" if close > rng_high
        for seed_val in [end_bar['low'], end_bar['high'], end_bar['close']]:
            s_l3a = s_l3b = s_l2a = s_l2b = s_l1a = s_l1b = seed_val
            for t in range(t_end + dt, ts('19:26:45') + dt, dt):
                if t in by_time:
                    cl = by_time[t]['close']
                    s_l3a += a_l3a * (cl - s_l3a)
                    s_l3b += a_l3b * (cl - s_l3b)
                    s_l2a += a_l2a * (cl - s_l2a)
                    s_l2b += a_l2b * (cl - s_l2b)
                    s_l1a += a_l1a * (cl - s_l1a)
                    s_l1b += a_l1b * (cl - s_l1b)
            
            diff = abs(s_l3a - 30868.31) + abs(s_l3b - 30868.29) + abs(s_l2a - 30868.49) + abs(s_l2b - 30868.43) + abs(s_l1a - 30869.16) + abs(s_l1b - 30868.98)
            if diff < 0.1:
                print(f"EXACT HIT: dt={dt}, END={end_str}, seed={seed_val}, C={c_final} -> diff={diff:.4f}")
                print(f"  3A: {s_l3a:.2f}, 3B: {s_l3b:.2f} | 2A: {s_l2a:.2f}, 2B: {s_l2b:.2f} | 1A: {s_l1a:.2f}, 1B: {s_l1b:.2f}")

