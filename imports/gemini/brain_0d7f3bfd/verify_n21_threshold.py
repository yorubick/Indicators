import json
from pathlib import Path

# Verify the n < 21 threshold across all known cases
print("=== VERIFYING n < 21 FALLBACK vs n >= 21 STRUCTURAL ENGINE ===")
print("Cases with n < 21:")
cases_under_21 = [
    # 1m Oct 12 morning
    ("12 Oct Morn 1m", "04:45-04:50", 60, 6, 60.0),
    ("12 Oct Morn 1m", "04:45-05:00", 60, 16, 60.0),
    ("12 Oct Morn 1m", "04:45-05:03", 60, 19, 62.29508197),
    ("12 Oct Morn 1m", "04:45-05:04", 60, 20, 65.57377049),
    # 1m Oct 12 evening
    ("12 Oct Even 1m", "19:00-19:01", 60, 2, 60.0),
    ("12 Oct Even 1m", "19:00-19:02", 60, 3, 60.0),
    ("12 Oct Even 1m", "19:00-19:03", 60, 4, 60.0),
    ("12 Oct Even 1m", "19:00-19:07", 60, 8, 60.0),
    ("12 Oct Even 1m", "19:00-19:11", 60, 12, 60.0),
    ("12 Oct Even 1m", "19:00-19:15", 60, 16, 60.0),
    ("12 Oct Even 1m", "19:00-19:16", 60, 17, 60.0),
    ("12 Oct Even 1m", "19:00-19:17", 60, 18, 60.0),
    ("12 Oct Even 1m", "19:00-19:18", 60, 19, 62.29508197),
    ("12 Oct Even 1m", "19:00-19:19", 60, 20, 65.57377049),
    # 1m Oct 13 evening
    ("13 Oct Even 1m", "19:00-19:18", 60, 19, 62.29508197),
    ("13 Oct Even 1m", "19:00-19:19", 60, 20, 65.57377049),
    # 15s Oct 12 evening
    ("12 Oct Even 15s", "19:00-19:04:30", 15, 19, 15.57377049),
    ("12 Oct Even 15s", "19:00-19:04:45", 15, 20, 16.39344262),
    ("12 Oct Even 15s", "19:18-19:20", 15, 9, 15.0),
]

all_match = True
for name, rng_str, dt, n, c_meas in cases_under_21:
    c_pred = max(float(dt), n * dt * 10.0 / 183.0)
    err = abs(c_meas - c_pred)
    if err > 1e-6:
        all_match = False
    print(f"{name:16s} | {rng_str:14s} | dt={dt:2d} | n={n:2d} | C_meas={c_meas:12.8f} | C_pred={c_pred:12.8f} | err={err:10.2e}")

print("\nAll 19 cases under 21 bars match the formula C = max(dt, n * dt * 10 / 183):", all_match)
