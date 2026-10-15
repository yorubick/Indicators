import csv
import json

csv_path = r"G:\trading\guias\analisis\manual\Lite_1903_192300_1m_b.csv"
rows = {}
with open(csv_path, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows[int(r["time"])] = r

sorted_times = sorted(rows.keys())

# Let's inspect the 3 benchmark series:
# Series 1: START 19:01
# Series 2: START 19:02
# Series 3: START 19:03

series_info = [
    ("START 19:01", 1791831660, [(21, 1791832860, 77), (22, 1791832920, 77), (23, 1791832980, 77), (24, 1791833040, 77)]),
    ("START 19:02", 1791831720, [(21, 1791832920, 50), (22, 1791832980, 52), (23, 1791833040, 55)]),
    ("START 19:03", 1791831780, [(21, 1791832980, 50), (22, 1791833040, 52), (23, 1791833100, 71), (24, 1791833160, 135)]),
]

print("AUDIT: Evaluating Candidate State Descriptors across START 19:01, 19:02, 19:03")
print("=" * 80)

for name, t_start, points in series_info:
    print(f"\n>>> {name} <<<")
    window_all = [t for t in sorted_times if t >= t_start]
    
    start_r = rows[t_start]
    s_h = float(start_r["high"])
    s_l = float(start_r["low"])
    s_c = float(start_r["close"])
    s_o = float(start_r["open"])
    s_rng = s_h - s_l
    
    for p_n, p_t, p_C in points:
        sub_times = [t for t in window_all if t <= p_t]
        highs = [float(rows[t]["high"]) for t in sub_times]
        lows = [float(rows[t]["low"]) for t in sub_times]
        closes = [float(rows[t]["close"]) for t in sub_times]
        
        w_h = max(highs)
        w_l = min(lows)
        w_rng = w_h - w_l
        
        # Invariant 1: Ratio of Start Candle Range to Total Range
        ratio_start_rng = s_rng / w_rng if w_rng > 0 else 0
        
        # Invariant 2: Relative position of Start Close in Window
        pos_start_c = (s_c - w_l) / w_rng if w_rng > 0 else 0
        
        # Invariant 3: Index of global High and Low from START (in bars)
        idx_h = highs.index(w_h)
        idx_l = lows.index(w_l)
        
        # Invariant 4: Bars since last new extreme made
        # Let's track when the last new high or low occurred
        last_new_ext_bar = 0
        curr_h = highs[0]
        curr_l = lows[0]
        for b_idx in range(1, len(sub_times)):
            if highs[b_idx] > curr_h:
                curr_h = highs[b_idx]
                last_new_ext_bar = b_idx
            if lows[b_idx] < curr_l:
                curr_l = lows[b_idx]
                last_new_ext_bar = b_idx
                
        bars_since_last_ext = (len(sub_times) - 1) - last_new_ext_bar
        
        # Invariant 5: Net displacement ratio (Close_END - Open_START) / Window_Range
        disp_ratio = (closes[-1] - s_o) / w_rng if w_rng > 0 else 0
        
        print(f"n={p_n:2d} (C={p_C:3d}) | StartRngRatio={ratio_start_rng:.3f} | StartClosePos={pos_start_c:.3f} | "
              f"IdxH={idx_h:2d} IdxL={idx_l:2d} | BarsSinceExt={bars_since_last_ext:2d} | DispRatio={disp_ratio:+.3f}")
