import csv
from datetime import datetime, timezone
import numpy as np

# Load candles from 15s data
with open('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

by_time = {int(r['time']): {k: float(r[k]) for k in ('open', 'high', 'low', 'close')} for r in rows}

def ts(t_str):
    return int(datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

# Target at 19:26:45
target_l3a = 30866.77
target_l3b = 30866.63
t_target = ts('19:26:45')

print(f"Target at 19:26:45: Lane 3 A = {target_l3a}, Lane 3 B = {target_l3b}\n")

# Possible STARTs and ENDs to test
starts = ['18:54:00', '18:55:00', '19:00:00', '19:03:00', '19:03:15', '19:03:30', '19:03:45', '19:04:00']
ends = ['19:20:00', '19:21:00', '19:22:00', '19:23:00', '19:23:15', '19:23:30', '19:23:45']

# Also known C values for these pairs
# Let's test a grid of C values from 10 to 150 for each candidate END
results = []

for end_str in ends:
    t_end = ts(end_str)
    if t_end not in by_time:
        continue
    
    end_bar = by_time[t_end]
    
    # Seeds: Bullish uses end_bar['low'], Bearish uses end_bar['high']
    for seed_type, seed_val in [('low (bull)', end_bar['low']), ('high (bear)', end_bar['high']), ('close', end_bar['close'])]:
        # Test C from 10 to 150
        for c_val in np.arange(10.0, 150.0, 0.05):
            # In 15s chart, resolution dt = 15
            len_l3a = (72.0 / 3.0) * (c_val / 15.0)
            len_l3b = (89.0 / 3.0) * (c_val / 15.0)
            
            a_l3a = 2.0 / (len_l3a + 1.0)
            a_l3b = 2.0 / (len_l3b + 1.0)
            
            # Recurrence from t_end + 15 to t_target
            val_l3a = seed_val
            val_l3b = seed_val
            for t in range(t_end + 15, t_target + 15, 15):
                if t in by_time:
                    cl = by_time[t]['close']
                    val_l3a += a_l3a * (cl - val_l3a)
                    val_l3b += a_l3b * (cl - val_l3b)
            
            err_a = abs(val_l3a - target_l3a)
            err_b = abs(val_l3b - target_l3b)
            if err_a < 0.02 and err_b < 0.02:
                results.append({
                    'end': end_str,
                    'seed_type': seed_type,
                    'seed_val': seed_val,
                    'C': round(c_val, 2),
                    'l3a': round(val_l3a, 4),
                    'l3b': round(val_l3b, 4),
                    'err_a': round(err_a, 4),
                    'err_b': round(err_b, 4),
                    'total_err': round(err_a + err_b, 4)
                })

results.sort(key=lambda x: x['total_err'])
print(f"Found {len(results)} matches with error < 0.02:")
for r in results[:10]:
    print(r)
