import csv, json
from pathlib import Path

# Let's test the two-regime formula on the entire 1m series from 19:00:
# 19:01 (2 bars): C = 60
# 19:02 (3 bars): C = 60
# 19:03 (4 bars): C = 60
# 19:07 (8 bars): C = 60
# 19:11 (12 bars): C = 60
# 19:15 (16 bars): C = 60
# 19:16 (17 bars): C = 60
# 19:17 (18 bars): C = 60
# 19:18 (19 bars): C = 62.29508197
# 19:19 (20 bars): C = 65.57377049
# 19:20 (21 bars): C = 77.0

cases_1900 = [
    (2, 60.0),
    (3, 60.0),
    (4, 60.0),
    (8, 60.0),
    (12, 60.0),
    (16, 60.0),
    (17, 60.0),
    (18, 60.0),
    (19, 62.29508197),
    (20, 65.57377049),
    (21, 77.0),
]

dt = 60
slope = 200.0 / (dt + 1) # 200 / 61 = 3.2786885

print("=== TESTING TWO REGIME BEHAVIOR ON 19:00-19:20 ===")
for n, c_actual in cases_1900:
    c_time = n * slope
    # For n <= 20, Range was <= 23.5 pts
    # For n = 21, Range was 24.5 pts (98 ticks)
    c_pred_time = max(float(dt), c_time)
    print(f"Bars: {n:2d} | c_time: {c_time:6.2f} | max(60, c_time): {c_pred_time:6.2f} | Actual: {c_actual:6.2f} | Diff: {abs(c_actual - c_pred_time):6.4f}")
