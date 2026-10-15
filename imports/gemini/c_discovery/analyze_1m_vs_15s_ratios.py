import numpy as np

# Let's print detailed analysis of C_1m vs C_15s
# n_1m: number of 1m bars from START 19:03 to END
# For n = 21..33:
# START = 19:03.
# END: 19:23 (20 min = 1200s, or 21 bars: 19:03..19:23 is 21 bars inclusive)
# Duration T = (END - START) in seconds

cases_data = [
    {"n": 21, "END": "19:23", "C_1m": 50, "C_15s": 87.9},
    {"n": 22, "END": "19:24", "C_1m": 52, "C_15s": 66.7},
    {"n": 23, "END": "19:25", "C_1m": 71, "C_15s": 88.0},
    {"n": 24, "END": "19:26", "C_1m": 135, "C_15s": 88.0},
    {"n": 25, "END": "19:27", "C_1m": 130, "C_15s": 79.3},
    {"n": 26, "END": "19:28", "C_1m": 88, "C_15s": 102.3},
    {"n": 27, "END": "19:29", "C_1m": 135, "C_15s": 123.2},
    {"n": 28, "END": "19:30", "C_1m": 112, "C_15s": 67.2},
    {"n": 29, "END": "19:31", "C_1m": 136, "C_15s": 87.0},
    {"n": 30, "END": "19:32", "C_1m": 112, "C_15s": 105.4},
    {"n": 31, "END": "19:33", "C_1m": 112, "C_15s": 86.9},
    {"n": 32, "END": "19:34", "C_1m": 135, "C_15s": 123.0},
    {"n": 33, "END": "19:35", "C_1m": 112, "C_15s": 87.1},
]

print(f"{'n':>2} | {'END':>5} | {'T (s)':>5} | {'T/18.3':>6} | {'C_1m':>5} | {'C_15s':>6} | {'Diff':>5} | {'C_1m - T/18.3':>14} | {'C_15s - T/18.3':>15}")
print("-" * 80)
for c in cases_data:
    n = c["n"]
    m_diff = int(c["END"].split(":")[1]) - 3 # minutes from 19:03
    T_sec = m_diff * 60
    t_over_183 = T_sec / 18.3
    c1m = c["C_1m"]
    c15 = c["C_15s"]
    diff = c1m - c15
    res_1m = c1m - t_over_183
    res_15 = c15 - t_over_183
    print(f"{n:>2} | {c['END']:>5} | {T_sec:>5} | {t_over_183:>6.1f} | {c1m:>5} | {c15:>6.1f} | {diff:>5.1f} | {res_1m:>14.1f} | {res_15:>15.1f}")
