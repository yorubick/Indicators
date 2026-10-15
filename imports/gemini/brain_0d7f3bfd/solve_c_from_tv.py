import csv, datetime
from pathlib import Path
import numpy as np

p = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

# Target at 19:26:45
target_l3a = 30866.77
target_l3b = 30866.63
t_breakout = ts('19:26:45')

# Let's test possible END timestamps: 19:20:00, 19:22:00, 19:23:00, 19:23:30, 19:23:45
test_ends = ['19:20:00', '19:22:00', '19:22:45', '19:23:00', '19:23:30', '19:23:45']

# Map times to rows
c_map = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows}

print("=== SOLVING FOR C FROM THE OBSERVED VALUES (Lane 3 A: 30866.77, Lane 3 B: 30866.63) ===")

for end_str in test_ends:
    t_end = ts(end_str)
    if t_end not in c_map:
        continue
    endpoint = c_map[t_end]
    
    # In bullish breakout, seed is endpoint['low']
    seed = endpoint['low']
    
    # We iterate over C from 50.0 to 120.0 with step 0.1
    best_c = None
    best_err = 1e9
    best_l3a = None
    best_l3b = None
    
    for c_cand in np.arange(50.0, 120.0, 0.05):
        # In 15s chart, dt = 15
        len_l3a = (72.0 / 3.0) * (c_cand / 15.0)  # 24 * c / 15 = 1.6 * c
        len_l3b = (89.0 / 3.0) * (c_cand / 15.0)  # (89/3) * c / 15
        
        a_l3a = 2.0 / (len_l3a + 1.0)
        a_l3b = 2.0 / (len_l3b + 1.0)
        
        val_l3a = seed
        val_l3b = seed
        
        for t in range(t_end + 15, t_breakout + 15, 15):
            if t in c_map:
                cl = c_map[t]['close']
                val_l3a += a_l3a * (cl - val_l3a)
                val_l3b += a_l3b * (cl - val_l3b)
                
        err = abs(val_l3a - target_l3a) + abs(val_l3b - target_l3b)
        if err < best_err:
            best_err = err
            best_c = c_cand
            best_l3a = val_l3a
            best_l3b = val_l3b
            
    print(f"If END was {end_str} (Seed={seed}): Best C = {best_c:.2f} s | L3A = {best_l3a:.4f} (err={best_l3a - target_l3a:+.4f}), L3B = {best_l3b:.4f} (err={best_l3b - target_l3b:+.4f}) | total_err={best_err:.4f}")
