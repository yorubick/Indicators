from master_cases import dataset
import numpy as np

print("Testing Kaufman / Efficiency / Velocity formulas against C:")

# For each case, compute:
# rng = High - Low
# sum_tr = sum(TR)
# dur_s = (n - 1) * dt
# efficiency = rng / sum_tr
# net_eff = abs(close - open) / sum_tr
# what about dur_s * efficiency?
# what about dur_s / (sum_tr / rng)?

results = []
for d in dataset:
    sub = d['sub']
    n = len(sub)
    dt = d['dt']
    C = d['C']
    h = np.array([x['high'] for x in sub])
    l = np.array([x['low'] for x in sub])
    c = np.array([x['close'] for x in sub])
    o = np.array([x['open'] for x in sub])
    
    rng = h.max() - l.min()
    bar_rng = h - l
    tr = np.maximum.reduce([bar_rng[1:], abs(h[1:] - c[:-1]), abs(l[1:] - c[:-1])]) if n > 1 else np.array([bar_rng[0]])
    sum_tr = tr.sum()
    dur_s = (n - 1) * dt
    
    eff = rng / sum_tr
    est1 = dur_s * eff
    est2 = dur_s * (rng / sum_tr)**2
    est3 = sum_tr / (rng / dur_s) if rng > 0 else 0
    
    # ratio C / est1
    ratio1 = C / est1 if est1 > 0 else 0
    results.append({
        's': d['s'], 'e': d['e'], 'dt': dt, 'C': C,
        'dur_s': dur_s, 'rng': rng, 'sum_tr': sum_tr,
        'eff': eff, 'est1': est1, 'ratio1': ratio1
    })

print(f"{'START':8s} {'END':8s} {'dt':3s} | {'C':4s} | {'dur_s':6s} | {'rng':6s} {'sum_tr':7s} | {'eff':6s} | {'dur*eff':8s} | {'ratio':6s}")
for r in results[:20]:
    print(f"{r['s']:8s} {r['e']:8s} {r['dt']:3d} | {r['C']:4d} | {r['dur_s']:6d} | {r['rng']:6.2f} {r['sum_tr']:7.2f} | {r['eff']:6.4f} | {r['est1']:8.2f} | {r['ratio1']:6.3f}")
