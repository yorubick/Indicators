import csv
import numpy as np

csv_path = r"G:\trading\guias\analisis\manual\Lite_1903_192300_1m_b.csv"
rows = {}
with open(csv_path, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows[int(r["time"])] = r

sorted_times = sorted(rows.keys())

series = [
    ("19:01", 1791831660, [(21, 1791832860, 77), (22, 1791832920, 77), (23, 1791832980, 77), (24, 1791833040, 77)]),
    ("19:02", 1791831720, [(21, 1791832920, 50), (22, 1791832980, 52), (23, 1791833040, 55)]),
    ("19:03", 1791831780, [(21, 1791832980, 50), (22, 1791833040, 52), (23, 1791833100, 71), (24, 1791833160, 135)]),
]

print("Testing Dimensionless Invariant Accumulators:")
print("=" * 70)

# Accumulator 1: Cumulative Normalized Position Z = (Close - Low_run) / (High_run - Low_run)
# Accumulator 2: Count of bars above START candle High / below START candle Low
# Accumulator 3: Running Efficiency: (Close - Open_0) / Sum(TrueRange)
# Accumulator 4: Bars since last new High / Low within the window

for name, t_start, points in series:
    print(f"\n--- Series {name} ---")
    start_row = rows[t_start]
    start_h = float(start_row["high"])
    start_l = float(start_row["low"])
    start_c = float(start_row["close"])
    start_o = float(start_row["open"])
    
    run_h = start_h
    run_l = start_l
    
    # Trackers
    bars_above_start_h = 0
    bars_below_start_l = 0
    cum_z = 0.0
    cum_tr = 0.0
    
    window_times = [t for t in sorted_times if t >= t_start]
    prev_c = start_c
    
    for i, t in enumerate(window_times):
        r = rows[t]
        h = float(r["high"])
        l = float(r["low"])
        c = float(r["close"])
        
        run_h = max(run_h, h)
        run_l = min(run_l, l)
        rng = run_h - run_l
        z = (c - run_l) / rng if rng > 0 else 0.5
        cum_z += z
        
        tr = max(h - l, abs(h - prev_c), abs(l - prev_c))
        cum_tr += tr
        prev_c = c
        
        if c > start_h:
            bars_above_start_h += 1
        if c < start_l:
            bars_below_start_l += 1
            
        # Check matching points
        for p_n, p_t, p_C in points:
            if t == p_t:
                eff = (c - start_o) / cum_tr if cum_tr > 0 else 0
                avg_z = cum_z / (i + 1)
                print(f"n={p_n:2d} (C={p_C:3d}) | AvgZ={avg_z:.3f} | Eff={eff:+.3f} | BarsAboveStartH={bars_above_start_h:2d} | BarsBelowStartL={bars_below_start_l:2d}")
