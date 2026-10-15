import numpy as np
from master_cases import dataset

print(f"Total dataset cases: {len(dataset)}")

# Let's extract all candidate features for each case
rows = []
for d in dataset:
    sub = d['sub']
    n = len(sub)
    dt = d['dt']
    C = d['C']
    
    o = np.array([x['open'] for x in sub])
    h = np.array([x['high'] for x in sub])
    l = np.array([x['low'] for x in sub])
    c = np.array([x['close'] for x in sub])
    
    rng = h.max() - l.min()
    ticks = rng / 0.25
    dur_s = (n - 1) * dt
    net_change = c[-1] - o[0]
    net_abs = abs(net_change)
    
    # Bar ranges and TR
    bar_rng = h - l
    tr = np.maximum.reduce([bar_rng[1:], abs(h[1:] - c[:-1]), abs(l[1:] - c[:-1])]) if n > 1 else np.array([bar_rng[0]])
    sum_tr = tr.sum()
    mean_tr = tr.mean()
    sum_rng = bar_rng.sum()
    mean_rng = bar_rng.mean()
    
    # Extremes
    idx_h = int(np.argmax(h))
    idx_l = int(np.argmin(l))
    
    # Distance of extremes to END in seconds
    dist_h_end_s = (n - 1 - idx_h) * dt
    dist_l_end_s = (n - 1 - idx_l) * dt
    # Distance of extremes from START in seconds
    dist_s_h_s = idx_h * dt
    dist_s_l_s = idx_l * dt
    
    # Distance between extremes
    dist_hl_s = abs(idx_h - idx_l) * dt
    dist_hl_bars = abs(idx_h - idx_l)
    
    rows.append({
        's': d['s'], 'e': d['e'], 'dt': dt, 'C': C, 'n': n,
        'rng': rng, 'ticks': ticks, 'dur_s': dur_s,
        'net_change': net_change, 'net_abs': net_abs,
        'sum_tr': sum_tr, 'mean_tr': mean_tr, 'sum_rng': sum_rng, 'mean_rng': mean_rng,
        'dist_h_end_s': dist_h_end_s, 'dist_l_end_s': dist_l_end_s,
        'dist_s_h_s': dist_s_h_s, 'dist_s_l_s': dist_s_l_s,
        'dist_hl_s': dist_hl_s, 'dist_hl_bars': dist_hl_bars,
        'idx_h': idx_h, 'idx_l': idx_l
    })

print("Testing simple correlations with C across all 42 cases:")
keys = [k for k in rows[0].keys() if k not in ('s', 'e', 'C')]
C_vals = np.array([r['C'] for r in rows])

corrs = {}
for k in keys:
    vals = np.array([r[k] for r in rows], dtype=float)
    if np.std(vals) > 0 and np.std(C_vals) > 0:
        corr = np.corrcoef(vals, C_vals)[0, 1]
        corrs[k] = corr

for k, c in sorted(corrs.items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"{k:20s}: corr = {c:+.4f}")
