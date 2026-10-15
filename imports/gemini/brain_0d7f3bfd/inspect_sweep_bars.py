from master_cases import dataset
import numpy as np

# Let's inspect the 15s START sweep cases specifically (END = 19:20:00)
sweep_15s = [d for d in dataset if d['dt'] == 15 and d['e'] == '19:20:00']
print(f"15s START sweep count: {len(sweep_15s)}")

for d in sweep_15s:
    sub = d['sub']
    n = len(sub)
    C = d['C']
    h = np.array([x['high'] for x in sub])
    l = np.array([x['low'] for x in sub])
    c = np.array([x['close'] for x in sub])
    o = np.array([x['open'] for x in sub])
    
    # Let's check various counts:
    # 1. Number of up bars vs down bars
    up_bars = np.sum(c > o)
    down_bars = np.sum(c < o)
    # 2. Number of bars above range midpoint
    mid = (h.max() + l.min()) / 2
    above_mid = np.sum(c > mid)
    below_mid = np.sum(c < mid)
    # 3. Bars from start to first close > open
    # 4. Bars from start to local pivot
    print(f"START {d['s']} | C={C:3d} | n={n:3d} | up={up_bars:2d} dn={down_bars:2d} | abv_mid={above_mid:2d} blw_mid={below_mid:2d} | first_bar_c-o={c[0]-o[0]:+5.2f}")
