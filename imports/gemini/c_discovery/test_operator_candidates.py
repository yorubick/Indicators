import csv
from datetime import datetime, timezone
import numpy as np

# Load 15s bars from C_barrido_15s_start1902.csv
with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Build 1m bars from 18:50 to 19:40
t_start_build = int(datetime(2026, 10, 12, 18, 50, 0, tzinfo=timezone.utc).timestamp())
t_end_build = int(datetime(2026, 10, 12, 19, 40, 0, tzinfo=timezone.utc).timestamp())

bars_1m = []
for t in range(t_start_build, t_end_build + 60, 60):
    sub = [bars_15s[t + s] for s in [0, 15, 30, 45]]
    bars_1m.append({
        "time": t,
        "dt": datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"),
        "open": float(sub[0]["open"]),
        "high": max(float(b["high"]) for b in sub),
        "low": min(float(b["low"]) for b in sub),
        "close": float(sub[3]["close"]),
        "subbars": sub
    })

time_to_idx = {b["dt"]: i for i, b in enumerate(bars_1m)}

# Data points: 19:23 to 19:35 (n=21 to 33)
actual_1m = {
    "19:23": 50, "19:24": 52, "19:25": 71, "19:26": 135, "19:27": 130,
    "19:28": 88, "19:29": 135, "19:30": 112, "19:31": 136, "19:32": 112,
    "19:33": 112, "19:34": 135, "19:35": 112
}

actual_15s = {
    "19:23": 88, "19:24": 67, "19:25": 88, "19:26": 88, "19:27": 79,
    "19:28": 102, "19:29": 123, "19:30": 67, "19:31": 87, "19:32": 106,
    "19:33": 87, "19:34": 123, "19:35": 87
}

print("=== CANDIDATE OPERATORS FOR C ===")

# Candidate 1: The OLR / Swing Duration Operator
# Let's inspect the duration in bars from the previous local swing low to END bar
# A swing low is defined as low[1] < low[0] and low[1] < low[2]
# Or distance from window breakout

# Candidate 2: Quantized Dynamic Threshold
# For n >= 21 in 1m:
# C_base = round(T / 18.3)
# In 1m:
# T / 18.3 at 19:28 is 82.0
# T / 18.3 at 19:30 is 88.5
# T / 18.3 at 19:32 is 95.1
# T / 18.3 at 19:33 is 98.4
# T / 18.3 at 19:35 is 104.9

# Notice that the median of C / (T/18.3) or similar:
for dt in sorted(actual_1m.keys()):
    i = time_to_idx[dt]
    b = bars_1m[i]
    m_diff = int(dt.split(":")[1]) - 3
    T = m_diff * 60
    base = round(T / 18.3)
    c_obs = actual_1m[dt]
    diff = c_obs - base
    print(f"{dt} | T={T:4d}s | Base={base:3d} | C_obs={c_obs:3d} | Diff={diff:+3d} | C/Base={c_obs/base:.2f}")
