import csv
import json
from datetime import datetime, timezone
import numpy as np

# Load 15s bars
with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# 1. Dataset of 8 START shifts (END 19:33)
start_shifts = [
    ("19:03", "19:33", 87),
    ("19:08", "19:33", 70),
    ("19:10", "19:33", 66),
    ("19:13", "19:33", 66),
    ("19:15", "19:33", 77),
    ("19:18", "19:33", 39),
    ("19:23", "19:33", 33),
    ("19:28", "19:33", 16),
    ("19:30", "19:33", 15),
]

# 2. Dataset of 13 END variations (START 19:03)
end_sweep_1903 = [
    ("19:03", "19:23", 88),
    ("19:03", "19:24", 67),
    ("19:03", "19:25", 88),
    ("19:03", "19:26", 88),
    ("19:03", "19:27", 79),
    ("19:03", "19:28", 102),
    ("19:03", "19:29", 123),
    ("19:03", "19:30", 67),
    ("19:03", "19:31", 87),
    ("19:03", "19:32", 106),
    ("19:03", "19:33", 87),
    ("19:03", "19:34", 123),
    ("19:03", "19:35", 87),
]

# Combine all unique cases
all_cases = []
seen = set()
for s, e, c in start_shifts + end_sweep_1903:
    key = (s, e)
    if key not in seen:
        seen.add(key)
        all_cases.append((s, e, c))

print(f"Total Unique Cases Analyzed: {len(all_cases)}")
print("=" * 110)
print(f"{'START':<6} | {'END':<6} | {'T(s)':<5} | {'C_med':<5} | {'C_base':<6} | {'Delta':<6} | {'Low':<8} | {'t_from_low':<10} | {'tau_L/18.3':<10} | {'Range':<6} | {'Net':<6}")
print("-" * 110)

records = []
for s_str, e_str, c_obs in all_cases:
    s_h, s_m = map(int, s_str.split(":"))
    e_h, e_m = map(int, e_str.split(":"))
    t_start = int(datetime(2026, 10, 12, s_h, s_m, 0, tzinfo=timezone.utc).timestamp())
    t_end = int(datetime(2026, 10, 12, e_h, e_m, 45, tzinfo=timezone.utc).timestamp())
    
    # Subbars in window
    win_ts = range(t_start, t_end + 1, 15)
    win_bars = [bars_15s[t] for t in win_ts if t in bars_15s]
    
    # Exact timestamp difference in seconds: time_end - time_start
    t_end_00 = int(datetime(2026, 10, 12, e_h, e_m, 0, tzinfo=timezone.utc).timestamp())
    T_sec = t_end_00 - t_start
    c_base = max(15, round(T_sec * 10.0 / 183.0))
    delta_c = c_obs - c_base
    
    lows = [float(b["low"]) for b in win_bars]
    highs = [float(b["high"]) for b in win_bars]
    min_l = min(lows)
    max_h = max(highs)
    
    # Index of first occurrence of min_low
    idx_min_l = lows.index(min_l)
    t_min_l = win_ts[idx_min_l]
    # Time from global low to END
    tau_low = t_end - t_min_l + 15
    tau_low_scaled = tau_low * 10.0 / 183.0
    
    net_disp = float(win_bars[-1]["close"]) - float(win_bars[0]["open"])
    rng = max_h - min_l
    
    rec = {
        "start": s_str,
        "end": e_str,
        "T": T_sec,
        "C_obs": c_obs,
        "C_base": c_base,
        "Delta_C": delta_c,
        "min_low": min_l,
        "tau_low": tau_low,
        "tau_low_scaled": tau_low_scaled,
        "range": rng,
        "net": net_disp,
    }
    records.append(rec)
    
    print(f"{s_str:<6} | {e_str:<6} | {T_sec:<5} | {c_obs:<5} | {c_base:<6} | {delta_c:<6} | {min_l:<8.2f} | {tau_low:<10} | {tau_low_scaled:<10.2f} | {rng:<6.2f} | {net_disp:<6.2f}")

# Correlation analysis
deltas = [r["Delta_C"] for r in records]
tau_lows = [r["tau_low"] for r in records]
ranges = [r["range"] for r in records]
nets = [r["net"] for r in records]

print("\n=== CORRELACIONES LINEALES CON DELTA C ===")
print(f"Corr(Delta_C, tau_low)  : {np.corrcoef(deltas, tau_lows)[0,1]:.4f}")
print(f"Corr(Delta_C, range)    : {np.corrcoef(deltas, ranges)[0,1]:.4f}")
print(f"Corr(Delta_C, net)      : {np.corrcoef(deltas, nets)[0,1]:.4f}")
