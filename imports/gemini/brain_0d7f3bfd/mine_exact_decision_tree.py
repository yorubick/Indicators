import master_cases
import numpy as np

# Load dataset
dataset = [d for d in master_cases.dataset if d['bars'] >= 21]

print(f"Mining exact decision rules on {len(dataset)} cases of n >= 21...")

# Let's extract clean, discrete features for each case:
data = []
for d in dataset:
    sub = d['sub']
    H = max(b['high'] for b in sub)
    L = min(b['low'] for b in sub)
    Rng = H - L
    ticks = round(Rng * 4)
    
    O0 = sub[0]['open']
    H0 = sub[0]['high']
    L0 = sub[0]['low']
    C0 = sub[0]['close']
    
    C_end = sub[-1]['close']
    H_end = sub[-1]['high']
    L_end = sub[-1]['low']
    
    n = d['bars']
    dt = d['dt']
    C = d['C']
    
    # Structural features:
    # 1. Start relative position in 4ths (discount < 0.25, eq 0.25-0.75, premium > 0.75)
    start_pos = (O0 - L) / Rng
    
    # 2. Is start bar a local high or low?
    is_start_green = C0 >= O0
    
    # 3. Distance from start to global extreme
    idx_max = [b['high'] for b in sub].index(H)
    idx_min = [b['low'] for b in sub].index(L)
    
    # 4. End bar retracement
    end_ret = (H - C_end) / Rng
    
    # 5. Range per bar
    r_per_b = Rng / n
    
    data.append({
        'case': f"{d['s'][:5]}->{d['e'][:8]}",
        'C': C,
        'dt': dt,
        'n': n,
        'Rng': Rng,
        'ticks': ticks,
        'start_pos': start_pos,
        'end_ret': end_ret,
        'r_per_b': r_per_b,
        'idx_max': idx_max,
        'idx_min': idx_min,
        'is_green': is_start_green
    })

# Let's sort by C
data.sort(key=lambda x: x['C'])

print(f"{'Case':16s} | {'C':3s} | {'dt':2s} | {'n':3s} | {'Rng':5s} | {'Ticks':5s} | {'StartPos':8s} | {'EndRet':6s} | {'Rng/Bar':7s} | {'MinIdx':6s} | {'MaxIdx':6s}")
for d in data:
    print(f"{d['case']:16s} | {d['C']:3d} | {d['dt']:2d} | {d['n']:3d} | {d['Rng']:5.2f} | {d['ticks']:5d} | {d['start_pos']:8.2f} | {d['end_ret']:6.2f} | {d['r_per_b']:7.3f} | {d['idx_min']:6d} | {d['idx_max']:6d}")
