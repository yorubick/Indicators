import csv
from datetime import datetime, timezone
import numpy as np

# Load candles
with open('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

by_time = {int(r['time']): {k: float(r[k]) for k in ('open', 'high', 'low', 'close')} for r in rows}

def ts(t_str):
    return int(datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

t_end = ts('19:23:30')
t_target = ts('19:26:45')

observed = {
    'l3a': 30868.31,
    'l3b': 30868.29,
    'l2a': 30868.49,
    'l2b': 30868.43,
    'l1a': 30869.16,
    'l1b': 30868.98
}

print("Searching for the exact recurrence that produced the user's observed values:")
print(observed)

# Let's test seeds:
# In Pine script Lab v4.0:
# If C = 62.0:
# What does Lab v4.0 do?
# Let's check Lab v4.0 code for recurrence!
# In Lab v4.0:
# if is_end_bar:
#   s_bull_l3a := end_low, ...
# if time > end_time:
#   s_bull_l3a := s_bull_l3a + a_lite_l3a * (close - s_bull_l3a)
# But wait! What candle is is_end_bar?
# If time == end_time (19:23:30):
# is_end_bar is true at 19:23:30!
# What is end_low? In candle 19:23:30: low = 30864.25!
# But wait, what if the chart is 1 minute?
# In 1 minute, the candle of 19:23:30 does NOT exist! In 1m, the candle is 19:23:00!
# What if the user is on 15s?
# In 15s, let's see how Lab v4 calculates with C = 62.0!

for dt in [15, 60]:
    c_val = 62.0
    p3a = (72.0 / 3.0) * (c_val / dt)
    p3b = (89.0 / 3.0) * (c_val / dt)
    p2a = (72.0 / 9.0) * (c_val / dt)
    p2b = (89.0 / 9.0) * (c_val / dt)
    p1a = (72.0 / 27.0) * (c_val / dt)
    p1b = (89.0 / 27.0) * (c_val / dt)
    
    a3a, a3b = 2.0 / (p3a + 1.0), 2.0 / (p3b + 1.0)
    a2a, a2b = 2.0 / (p2a + 1.0), 2.0 / (p2b + 1.0)
    a1a, a1b = 2.0 / (p1a + 1.0), 2.0 / (p1b + 1.0)
    
    # Let's test various seeds and start times
    for seed_val in [30864.25, 30868.75, 30866.50, 30868.25, 30870.75, 30849.00]:
        # Recurrence from t_end
        v3a, v3b, v2a, v2b, v1a, v1b = [seed_val]*6
        for t in range(t_end + 15, t_target + 15, 15):
            cl = by_time[t]['close']
            v3a += a3a * (cl - v3a)
            v3b += a3b * (cl - v3b)
            v2a += a2a * (cl - v2a)
            v2b += a2b * (cl - v2b)
            v1a += a1a * (cl - v1a)
            v1b += a1b * (cl - v1b)
        
        diff = max(abs(v3a - observed['l3a']), abs(v3b - observed['l3b']),
                   abs(v2a - observed['l2a']), abs(v2b - observed['l2b']),
                   abs(v1a - observed['l1a']), abs(v1b - observed['l1b']))
        if diff < 0.05:
            print(f"MATCH with dt={dt}, seed={seed_val}, C={c_val}: max_diff={diff:.4f}")
            print(f"  3A={v3a:.2f}, 3B={v3b:.2f}, 2A={v2a:.2f}, 2B={v2b:.2f}, 1A={v1a:.2f}, 1B={v1b:.2f}")
