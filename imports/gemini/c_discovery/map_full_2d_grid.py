import csv
import glob
import os
import re
from datetime import datetime, timezone
from scipy.optimize import brentq

# 1. Load all 60s bars for Oct 12
bars_by_time = {}
# First from Lite_1904_193000_1m_b.csv
with open(r"G:\trading\guias\analisis\manual\Lite_1904_193000_1m_b.csv", "r") as f:
    for r in csv.DictReader(f):
        t = int(r["time"])
        dt_val = datetime.fromtimestamp(t, tz=timezone.utc)
        if dt_val.strftime("%Y-%m-%d") == "2026-10-12":
            bars_by_time[t] = {
                "time": t,
                "open": float(r["open"]),
                "high": float(r["high"]),
                "low": float(r["low"]),
                "close": float(r["close"])
            }

times = sorted(bars_by_time.keys())
time_map = {datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"): t for t in times}

factors = {
    "Lane 3 A": 24.0,
    "Lane 3 B": 89.0 / 3.0,
    "Lane 2 A": 8.0,
    "Lane 2 B": 89.0 / 9.0,
    "Lane 1 A": 72.0 / 27.0,
    "Lane 1 B": 89.0 / 27.0,
}

def simulate_curve(t_end, C_val, lane_name, t_eval, seed):
    dt = 60.0
    b0 = factors[lane_name]
    alpha = 2.0 / ((b0 * C_val / dt) + 1.0)
    state = seed
    eval_bars = [bars_by_time[t] for t in times if t_end < t <= t_eval]
    for b in eval_bars:
        state += alpha * (b["close"] - state)
    return state

def solve_C_from_bar(t_end, lane_name, observed_val, t_eval, seed):
    def f(c):
        return simulate_curve(t_end, c, lane_name, t_eval, seed) - observed_val
    try:
        return brentq(f, 5.0, 500.0)
    except Exception:
        return None

# Find all 1m CSVs in manual
files = glob.glob(r"G:\trading\guias\analisis\manual\Lite_*_1m_*.csv")
print(f"Total 1m files in manual: {len(files)}")

results = {}

for fpath in files:
    fname = os.path.basename(fpath)
    # Parse start and end from filename: Lite_1900_1920_1m_a.csv or Lite_1900_192100_1m_a.csv
    m = re.match(r"Lite_(\d{4})_(\d{4,6})_1m_([a-z0-9]+)\.csv", fname)
    if not m:
        continue
    start_str = m.group(1) # e.g. 1900
    end_str = m.group(2)[:4] # e.g. 1920
    tag = m.group(3)
    
    start_hhmm = f"{start_str[:2]}:{start_str[2:]}"
    end_hhmm = f"{end_str[:2]}:{end_str[2:]}"
    
    if start_hhmm not in time_map or end_hhmm not in time_map:
        continue
        
    t_start = time_map[start_hhmm]
    t_end = time_map[end_hhmm]
    
    if t_start >= t_end:
        continue
        
    # Read rows from CSV to find the first valid curve plot
    with open(fpath, "r") as f:
        reader = csv.DictReader(f)
        solved_c = None
        for r in reader:
            t_curr = int(r["time"])
            if t_curr > t_end and r.get("Lane 3 A") and r["Lane 3 A"].strip() != "":
                l3a = float(r["Lane 3 A"])
                # We need seed: low of end bar for bull breakout, high for bear
                seed_low = bars_by_time[t_end]["low"]
                seed_high = bars_by_time[t_end]["high"]
                
                # Try bull breakout first
                c_sol = solve_C_from_bar(t_end, "Lane 3 A", l3a, t_curr, seed_low)
                if c_sol is None or c_sol < 5.0 or c_sol > 499.0:
                    c_sol = solve_C_from_bar(t_end, "Lane 3 A", l3a, t_curr, seed_high)
                    
                if c_sol is not None:
                    solved_c = c_sol
                    break
        if solved_c is not None:
            key = (start_hhmm, end_hhmm)
            if key not in results:
                results[key] = []
            results[key].append(solved_c)

print(f"\nUnique (START, END) pairs mapped: {len(results)}")
print(f"{'START':7} | {'END':7} | {'n':3} | {'C_solved':8} | {'C_round':7}")
print("-" * 45)
for (s, e) in sorted(results.keys()):
    vals = results[(s, e)]
    mean_c = sum(vals) / len(vals)
    n_bars = (time_map[e] - time_map[s]) // 60 + 1
    print(f"{s:7} | {e:7} | {n_bars:3d} | {mean_c:8.3f} | {round(mean_c):7d}")
