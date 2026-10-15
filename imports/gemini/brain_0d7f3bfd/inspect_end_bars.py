from master_cases import dataset
import numpy as np

end_15s = [d for d in dataset if d['dt'] == 15 and d['s'] == '18:55:00']
print(f"15s END sweep count: {len(end_15s)}")

for d in end_15s:
    sub = d['sub']
    n = len(sub)
    C = d['C']
    h = np.array([x['high'] for x in sub])
    l = np.array([x['low'] for x in sub])
    c = np.array([x['close'] for x in sub])
    o = np.array([x['open'] for x in sub])
    
    up_bars = np.sum(c > o)
    down_bars = np.sum(c < o)
    mid = (h.max() + l.min()) / 2
    above_mid = np.sum(c > mid)
    below_mid = np.sum(c < mid)
    
    print(f"END {d['e']} | C={C:3d} | n={n:3d} | up={up_bars:2d} dn={down_bars:2d} | abv_mid={above_mid:2d} blw_mid={below_mid:2d} | last_bar_c-o={c[-1]-o[-1]:+5.2f} high={h.max():.2f}")
