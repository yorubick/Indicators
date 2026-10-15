import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

# Get all 60s bars
case = [c for c in master["cases"] if c.get("id") == "20261012_190400_193000_60s"][0]
bars = {b["time"]: b for b in case["OHLCV"]}
case0 = [c for c in master["cases"] if c.get("id") == "20261012_190000_192400_60s"][0]
bars.update({b["time"]: b for b in case0["OHLCV"]})

from datetime import datetime, timezone
times = sorted(bars.keys())
time_map = {datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"): t for t in times}

# Compare START 19:03 vs START 19:04 at each END from 19:23 to 19:30
print("END   | 19:03 (n, C)   | 19:04 (n, C)   | 19:03 High/Low       | 19:04 High/Low")
print("-" * 75)

# We know:
# 19:03: 19:23 (21, 50), 19:24 (22, 52), 19:25 (23, 71), 19:26 (24, 135)
# 19:04: 19:24 (21, 50), 19:25 (22, 71), 19:26 (23, 71), 19:27 (24, 71), 19:28 (25, 128), 19:29 (26, 134), 19:30 (27, 109)

c_1903 = {
    "19:23": (21, 50),
    "19:24": (22, 52),
    "19:25": (23, 71),
    "19:26": (24, 135)
}
c_1904 = {
    "19:24": (21, 50),
    "19:25": (22, 71),
    "19:26": (23, 71),
    "19:27": (24, 71),
    "19:28": (25, 128),
    "19:29": (26, 134),
    "19:30": (27, 109)
}

for end_m in ["19:23", "19:24", "19:25", "19:26", "19:27", "19:28", "19:29", "19:30"]:
    t_end = time_map.get(end_m)
    if not t_end:
        continue
    
    # 19:03 window
    t_s03 = time_map["19:03"]
    w03 = [bars[t] for t in times if t_s03 <= t <= t_end]
    h03 = max(b["high"] for b in w03)
    l03 = min(b["low"] for b in w03)
    c03_str = f"n={len(w03)}, C={c_1903.get(end_m, ('?', '?'))[1]}"
    
    # 19:04 window
    t_s04 = time_map["19:04"]
    w04 = [bars[t] for t in times if t_s04 <= t <= t_end]
    h04 = max(b["high"] for b in w04)
    l04 = min(b["low"] for b in w04)
    c04_str = f"n={len(w04)}, C={c_1904.get(end_m, ('?', '?'))[1]}"
    
    print(f"{end_m} | {c03_str:14} | {c04_str:14} | H:{h03:8.2f} L:{l03:8.2f} | H:{h04:8.2f} L:{l04:8.2f}")
