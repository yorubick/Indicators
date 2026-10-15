import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

# Find 19:01 -> 19:23 (C=77) and 19:02 -> 19:24 (C=55)
c77 = next(c for c in data['cases'] if c['START'].startswith('2026-10-12T19:01') and c['bars'] == 23)
c55 = next(c for c in data['cases'] if c['START'].startswith('2026-10-12T19:02') and c['bars'] == 23)

ohlc77 = c77['OHLC']
ohlc55 = c55['OHLC']

print("=== BAR BY BAR COMPARISON ===")
print("Index | Time 77  | C 77     | Time 55  | C 55     | Diff Close")
print("-" * 65)
for i in range(23):
    t77 = ohlc77[i]['time']
    c_p77 = ohlc77[i]['close']
    t55 = ohlc55[i]['time']
    c_p55 = ohlc55[i]['close']
    print(f"{i:5d} | {t77} | {c_p77:8.2f} | {t55} | {c_p55:8.2f} | {c_p55 - c_p77:8.2f}")

# Notice:
# ohlc77 has bars from 19:01 to 19:23
# ohlc55 has bars from 19:02 to 19:24
# They overlap from 19:02 to 19:23 (22 common bars!)
# The unique bar in 77 is 19:01 (the first bar).
# The unique bar in 55 is 19:24 (the last bar).

print("\n=== UNIQUE BARS ===")
print("Bar 19:01 (only in 77):", ohlc77[0])
print("Bar 19:24 (only in 55):", ohlc55[-1])

# Let's compare comprehensive statistics:
def get_stats(ohlc):
    o = np.array([x['open'] for x in ohlc])
    h = np.array([x['high'] for x in ohlc])
    l = np.array([x['low'] for x in ohlc])
    c = np.array([x['close'] for x in ohlc])
    
    rng = np.max(h) - np.min(l)
    net = c[-1] - o[0]
    net_c = c[-1] - c[0]
    gross_path = np.sum(np.abs(np.diff(c)))
    er = abs(net_c) / gross_path if gross_path > 0 else 0
    
    trs = [h[0] - l[0]] + [max(h[i]-l[i], abs(h[i]-c[i-1]), abs(l[i]-c[i-1])) for i in range(1, len(c))]
    atr = np.mean(trs)
    sum_tr = np.sum(trs)
    
    # Cumulative variance / standard deviation of closes
    std_c = np.std(c)
    mean_c = np.mean(c)
    
    # First candle properties
    first_body = abs(c[0] - o[0])
    first_range = h[0] - l[0]
    first_dir = 1 if c[0] >= o[0] else -1
    
    # Start position in range:
    start_pos = (o[0] - np.min(l)) / rng
    
    # End position in range:
    end_pos = (c[-1] - np.min(l)) / rng
    
    # Center of mass (time-weighted price):
    t_weights = np.arange(len(c))
    com = np.sum(c * t_weights) / np.sum(t_weights)
    
    # Slope of linear regression of close
    slope, intercept = np.polyfit(np.arange(len(c)), c, 1)
    
    return {
        'range': rng,
        'net': net,
        'net_c': net_c,
        'gross_path': gross_path,
        'er': er,
        'atr': atr,
        'sum_tr': sum_tr,
        'std_c': std_c,
        'mean_c': mean_c,
        'first_body': first_body,
        'first_range': first_range,
        'first_dir': first_dir,
        'start_pos': start_pos,
        'end_pos': end_pos,
        'com': com,
        'slope': slope
    }

s77 = get_stats(ohlc77)
s55 = get_stats(ohlc55)

print("\n=== METRIC COMPARISON ===")
print(f"{'Metric':15s} | {'19:01 (C=77)':15s} | {'19:02 (C=55)':15s} | {'Difference':15s}")
print("-" * 65)
for k in s77:
    v77 = s77[k]
    v55 = s55[k]
    print(f"{k:15s} | {v77:15.4f} | {v55:15.4f} | {v55 - v77:15.4f}")
