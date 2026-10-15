import json
import math

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

# Get all 60s bars for Oct 12
bars_by_time = {}
for c in master["cases"]:
    if c.get("dt") == 60 and "2026-10-12" in c.get("START", ""):
        for b in c.get("OHLCV", []):
            bars_by_time[b["time"]] = b

from datetime import datetime, timezone
times = sorted(bars_by_time.keys())
time_map = {datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"): t for t in times}

# Define test episodes:
episodes = [
    ("19:01", "19:21", 21, 77),
    ("19:01", "19:22", 22, 77),
    ("19:01", "19:23", 23, 77),
    ("19:01", "19:24", 24, 77),
    ("19:02", "19:22", 21, 50),
    ("19:02", "19:23", 22, 52),
    ("19:02", "19:24", 23, 55),
    ("19:03", "19:23", 21, 50),
    ("19:03", "19:24", 22, 52),
    ("19:03", "19:25", 23, 71),
    ("19:03", "19:26", 24, 135),
    ("19:04", "19:24", 21, 50),
    ("19:04", "19:25", 22, 71),
    ("19:04", "19:26", 23, 71),
    ("19:04", "19:27", 24, 71),
    ("19:04", "19:28", 25, 128),
    ("19:04", "19:29", 26, 134),
    ("19:04", "19:30", 27, 109),
]

print(f"{'START':5} | {'END':5} | {'n':2} | {'C':3} | {'Rng':5} | {'VolTot':7} | {'AVWAP':8} | {'DistH':5} | {'DistL':5} | {'ER':5} | {'StartBody':9}")
print("-" * 80)

for s_str, e_str, n_exp, c_exp in episodes:
    t_s = time_map[s_str]
    t_e = time_map[e_str]
    w = [bars_by_time[t] for t in times if t_s <= t <= t_e]
    n_actual = len(w)
    
    h_max = max(b["high"] for b in w)
    l_min = min(b["low"] for b in w)
    rng = h_max - l_min
    vol_tot = sum(b["volume"] for b in w)
    vwap = sum(b["volume"] * (b["high"] + b["low"] + b["close"])/3.0 for b in w) / vol_tot
    
    h_idx = max(i for i, b in enumerate(w) if b["high"] == h_max)
    l_idx = min(i for i, b in enumerate(w) if b["low"] == l_min)
    
    # Cumulative path
    path = sum(abs(w[i]["close"] - w[i-1]["close"]) for i in range(1, len(w)))
    net_disp = abs(w[-1]["close"] - w[0]["open"])
    er = net_disp / path if path > 0 else 0
    
    start_body = w[0]["close"] - w[0]["open"]
    
    print(f"{s_str:5} | {e_str:5} | {n_exp:2d} | {c_exp:3d} | {rng:5.2f} | {vol_tot:7.0f} | {vwap:8.2f} | {h_idx:5d} | {l_idx:5d} | {er:5.3f} | {start_body:+9.2f}")
