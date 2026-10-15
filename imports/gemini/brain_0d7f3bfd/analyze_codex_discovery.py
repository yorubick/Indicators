import json, math
from pathlib import Path

# Analysis of Codex's finding:
# 19 bars: C = 3800 / 61 = 62.295081967213115
# 20 bars: C = 4000 / 61 = 65.57377049180328
# Difference: 200 / 61 = 3.278688524590164

print("=== ANALYSIS OF CODEX'S FRACTIONAL C DISCOVERY ===")
c19 = 3800 / 61
c20 = 4000 / 61
diff = c20 - c19

print(f"C(19): {c19:.10f}")
print(f"C(20): {c20:.10f}")
print(f"Diff:  {diff:.10f} = 200 / 61")

# Notice:
# 200 / 61 = 100 * (2 / 61) = 100 * alpha_60
# Why 100?
# In TradingView / Pine Script:
# Is it percentage? (100 * alpha)
# Or is 200 / 61 derived from:
# C = 100 * (2 / (dt + 1)) * bars?
# Let's check for other bar counts:
for n in range(1, 25):
    c_pred = n * 200 / 61
    print(f"Bars: {n:2d} -> C_lin: {c_pred:6.2f} (max(60, C): {max(60.0, c_pred):6.2f})")
