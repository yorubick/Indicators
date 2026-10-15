import csv
from datetime import datetime, timezone
import json
import numpy as np

# Load 15s bars from C_barrido_15s_start1902.csv
with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Build 1m bars from 19:03 to 19:36
t_start = int(datetime(2026, 10, 12, 19, 3, 0, tzinfo=timezone.utc).timestamp())
t_end_max = int(datetime(2026, 10, 12, 19, 36, 0, tzinfo=timezone.utc).timestamp())

bars_1m = {}
for t in range(t_start, t_end_max + 60, 60):
    sub = [bars_15s[t + s] for s in [0, 15, 30, 45]]
    bars_1m[t] = {
        "time": t,
        "dt": datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"),
        "open": float(sub[0]["open"]),
        "high": max(float(b["high"]) for b in sub),
        "low": min(float(b["low"]) for b in sub),
        "close": float(sub[3]["close"]),
        "subbars": sub
    }

# Observed C values
observed_1m = {
    "19:23": 50, "19:24": 52, "19:25": 71, "19:26": 135, "19:27": 130,
    "19:28": 88, "19:29": 135, "19:30": 112, "19:31": 136, "19:32": 112,
    "19:33": 112, "19:34": 135, "19:35": 112
}

observed_15s = {
    "19:23": 88, "19:24": 67, "19:25": 88, "19:26": 88, "19:27": 79,
    "19:28": 102, "19:29": 123, "19:30": 67, "19:31": 87, "19:32": 106,
    "19:33": 87, "19:34": 123, "19:35": 87
}

print("=========================================================================================")
print("EVALUACIÓN DE LA CONDICIÓN CINEMÁTICA E(t) EN LAS 13 VENTANAS (19:23 a 19:35 UTC)")
print("=========================================================================================")
print(f"{'n':>2} | {'END':>5} | {'Obs_1m':>6} | {'Obs_15s':>7} | {'Win_H':>8} | {'New_H?':>6} | {'Pos%':>6} | {'UWick':>5} | {'Sub_Max':>7} | {'E_cand':>6}")
print("-" * 89)

# Running window high
win_high = -1e9

results_eval = []

for m in range(23, 36):
    n = m - 2 # n=21..33
    dt_str = f"19:{m:02d}"
    t = int(datetime(2026, 10, 12, 19, m, 0, tzinfo=timezone.utc).timestamp())
    b = bars_1m[t]
    
    # Previous window high before this candle
    prev_win_h = win_high
    is_new_h = b["high"] >= prev_win_h if prev_win_h > 0 else True
    if b["high"] > win_high:
        win_high = b["high"]
        
    rng = b["high"] - b["low"]
    pos_pct = (b["close"] - b["low"]) / rng * 100.0 if rng > 0 else 50.0
    uwick = b["high"] - max(b["open"], b["close"])
    
    # Subbars
    sub = b["subbars"]
    sub_highs = [float(sb["high"]) for sb in sub]
    max_idx = int(np.argmax(sub_highs))
    sub_names = [":00", ":15", ":30", ":45"]
    max_sub = sub_names[max_idx]
    
    # Candidate rule:
    # E = 1 if is_new_h AND pos_pct >= 90.0 AND max_sub == ':45'
    e_cand = (is_new_h and pos_pct >= 90.0 and max_sub == ":45")
    
    obs1m = observed_1m[dt_str]
    obs15 = observed_15s[dt_str]
    
    results_eval.append({
        "n": n, "dt": dt_str, "obs_1m": obs1m, "obs_15s": obs15,
        "is_new_h": is_new_h, "pos_pct": pos_pct, "uwick": uwick,
        "max_sub": max_sub, "e_cand": e_cand
    })
    
    print(f"{n:>2} | {dt_str:>5} | {obs1m:>6} | {obs15:>7} | {b['high']:>8.2f} | {str(is_new_h):>6} | {pos_pct:>5.1f}% | {uwick:>5.2f} | {max_sub:>7} | {str(e_cand):>6}")
