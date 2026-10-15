from master_cases import dataset
import numpy as np

print("Testing ATR values across all 42 cases:")

def compute_atr(sub, length=14):
    h = np.array([x['high'] for x in sub])
    l = np.array([x['low'] for x in sub])
    c = np.array([x['close'] for x in sub])
    n = len(sub)
    tr = np.zeros(n)
    tr[0] = h[0] - l[0]
    for i in range(1, n):
        tr[i] = max(h[i] - l[i], abs(h[i] - c[i-1]), abs(l[i] - c[i-1]))
    # RMA (Wilder's smoothing)
    atr = np.zeros(n)
    atr[0] = tr[0]
    alpha = 1.0 / length
    for i in range(1, n):
        atr[i] = alpha * tr[i] + (1 - alpha) * atr[i-1]
    return atr

for d in dataset[:20]:
    sub = d['sub']
    C = d['C']
    dt = d['dt']
    atr14 = compute_atr(sub, 14)[-1]
    atr7 = compute_atr(sub, 7)[-1]
    rng = d['range']
    
    # What about rng / atr?
    ratio_14 = rng / atr14 if atr14 > 0 else 0
    ratio_7 = rng / atr7 if atr7 > 0 else 0
    
    print(f"{d['s']:8s} {d['e']:8s} {dt:2d}s | C={C:3d} | Rng={rng:5.2f} | ATR14={atr14:4.2f} R/ATR14={ratio_14:5.2f} | ATR7={atr7:4.2f} R/ATR7={ratio_7:5.2f}")
