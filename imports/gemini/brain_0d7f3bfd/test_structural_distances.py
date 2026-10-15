import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

long_cases = [c for c in d["cases"] if c["branch"] == "long"]

# Let's inspect the relationship between C and different time/bar distances:
# 1. Total span: n * dt (or (n-1)*dt)
# 2. Distance from lowest low to END
# 3. Distance from highest high to END
# 4. Distance from START to lowest low
# 5. Distance from START to highest high
# 6. Distance between extremes: |idx_high - idx_low| * dt

print(f"{'Case ID':30s} {'n':3s} {'C':5s} {'dt':3s} {'Dist_L_to_END':13s} {'Dist_H_to_END':13s} {'Dist_Ext':8s} {'H_minus_L':9s}")
for c in long_cases[:25]:
    dt = c["dt"]
    ohlc = c["OHLC"]
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    i_max = int(np.argmax(highs))
    i_min = int(np.argmin(lows))
    n = len(ohlc)
    dist_l_end = (n - 1 - i_min) * dt
    dist_h_end = (n - 1 - i_max) * dt
    dist_ext = abs(i_max - i_min) * dt
    rng = max(highs) - min(lows)
    print(f"{c['id']:30s} {n:3d} {int(c['C']):5d} {dt:3d} {dist_l_end:13d} {dist_h_end:13d} {dist_ext:8d} {rng:9.2f}")
