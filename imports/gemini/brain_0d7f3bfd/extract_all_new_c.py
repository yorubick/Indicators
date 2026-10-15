import csv, json
from pathlib import Path
import numpy as np

lanes = ['Lane 3 A', 'Lane 3 B', 'Lane 2 A', 'Lane 2 B', 'Lane 1 A', 'Lane 1 B']
bases = [72/3, 89/3, 72/9, 89/9, 72/27, 89/27]

def extract_c_lite(csv_path, dt=60):
    rows = list(csv.DictReader(open(csv_path, encoding='utf-8-sig')))
    # Filter rows that have all lanes
    valid = [r for r in rows if all(r.get(l, '') != '' for l in lanes)]
    if len(valid) < 5:
        return None, None, len(valid)
    
    # Check consecutive rows separated by dt
    c_estimates = []
    for lane, base in zip(lanes, bases):
        # Fit alpha: y[t] - y[t-1] = alpha * (close[t] - y[t-1])
        dy = []
        dx = []
        for i in range(1, len(valid)):
            t0 = int(valid[i-1]['time'])
            t1 = int(valid[i]['time'])
            if t1 - t0 == dt:
                y0 = float(valid[i-1][lane])
                y1 = float(valid[i][lane])
                c1 = float(valid[i]['close'])
                dy.append(y1 - y0)
                dx.append(c1 - y0)
        if len(dx) >= 3:
            dx = np.array(dx)
            dy = np.array(dy)
            # Least squares alpha = sum(dx * dy) / sum(dx * dx)
            denom = np.sum(dx * dx)
            if denom > 1e-12:
                alpha = np.sum(dx * dy) / denom
                if 0 < alpha < 1:
                    # alpha = 2 / (N + 1) -> N = 2/alpha - 1
                    N = 2.0 / alpha - 1.0
                    # N = base * C / dt -> C = N * dt / base
                    C = N * dt / base
                    c_estimates.append(C)
                    
    if c_estimates:
        mean_c = np.mean(c_estimates)
        std_c = np.std(c_estimates)
        return mean_c, std_c, len(valid)
    return None, None, len(valid)

manual_dir = Path('G:/trading/guias/analisis/manual')
print("=== EXTRACTING C FROM ALL NEW MANUAL CSVS ===")
for p in sorted(manual_dir.glob('Lite_*_a.csv')):
    c_val, c_std, n_rows = extract_c_lite(p)
    if c_val is not None:
        print(f"{p.name:32s} | C = {c_val:14.8f} (std={c_std:8.2e}) | rows={n_rows}")
    else:
        print(f"{p.name:32s} | No curves / pairs ({n_rows} rows)")
