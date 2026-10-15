import csv
import numpy as np

csv_path = r"G:\trading\guias\analisis\manual\Lite_1903_192300_1m_b.csv"
rows = {}
with open(csv_path, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows[int(r["time"])] = r

sorted_times = sorted(rows.keys())

# Define the targets:
# Series 19:01:
# END 19:21 (n=21) -> C = 77
# END 19:22 (n=22) -> C = 77
# END 19:23 (n=23) -> C = 77
# END 19:24 (n=24) -> C = 77
# Series 19:02:
# END 19:22 (n=21) -> C = 50
# END 19:23 (n=22) -> C = 52
# END 19:24 (n=23) -> C = 55
# Series 19:03:
# END 19:23 (n=21) -> C = 50
# END 19:24 (n=22) -> C = 52
# END 19:25 (n=23) -> C = 71
# END 19:26 (n=24) -> C = 135

series = [
    ("19:01", 1791831660, [(21, 1791832860, 77), (22, 1791832920, 77), (23, 1791832980, 77), (24, 1791833040, 77)]),
    ("19:02", 1791831720, [(21, 1791832920, 50), (22, 1791832980, 52), (23, 1791833040, 55)]),
    ("19:03", 1791831780, [(21, 1791832980, 50), (22, 1791833040, 52), (23, 1791833100, 71), (24, 1791833160, 135)]),
]

# Let's test various candidate accumulators initialized at START
# 1. EMA of close with various fixed alphas
# 2. Cumulative sum of true range / (range)
# 3. Accumulated directional movement (DM+, DM-)
# 4. Running efficiency / variance

def run_tests():
    print("Testing candidate state variables across the 3 series:")
    print("=" * 70)
    
    # Test 1: EMA of Close with alpha = 2/(length + 1)
    for length in [3, 5, 9, 14, 20]:
        alpha = 2.0 / (length + 1.0)
        print(f"\n--- Candidate: EMA(Close, length={length}) ---")
        for name, t_start, points in series:
            # Run from t_start
            window_times = [t for t in sorted_times if t >= t_start]
            state = float(rows[t_start]["close"])
            vals = []
            for t in window_times:
                c = float(rows[t]["close"])
                state += alpha * (c - state)
                # Check if t is in points
                for p_n, p_t, p_C in points:
                    if t == p_t:
                        vals.append((p_n, p_C, round(state, 2)))
            print(f"Series {name}: {vals}")

run_tests()
