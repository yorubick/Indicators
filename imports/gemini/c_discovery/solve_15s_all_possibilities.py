import csv
from datetime import datetime, timezone
from scipy.optimize import brentq
import numpy as np

# Load 15s bars
with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Official readings provided by user for n=33 (END 19:35, eval 19:36)
# Lane 3 A: 30896.10, Lane 3 B: 30895.99
# Lane 2 A: 30897.22, Lane 2 B: 30896.91
# Lane 1 A: 30899.97, Lane 1 B: 30899.26
obs_33 = {
    "Lane 3 A": 30896.10,
    "Lane 3 B": 30895.99,
    "Lane 2 A": 30897.22,
    "Lane 2 B": 30896.91,
    "Lane 1 A": 30899.97,
    "Lane 1 B": 30899.26,
}

factors = {
    "Lane 3 A": 24.0,           # Lane A Fast
    "Lane 3 B": 89.0 / 3.0,     # Lane A Slow
    "Lane 2 A": 8.0,            # Lane B Fast
    "Lane 2 B": 89.0 / 9.0,     # Lane B Slow
    "Lane 1 A": 72.0 / 27.0,    # Lane C Fast
    "Lane 1 B": 89.0 / 27.0,    # Lane C Slow
}

# Let's test different definitions of seed and updates for END 19:35, eval 19:36
t_end_00 = int(datetime(2026, 10, 12, 19, 35, 0, tzinfo=timezone.utc).timestamp())
t_end_45 = int(datetime(2026, 10, 12, 19, 35, 45, tzinfo=timezone.utc).timestamp())
t_eval_45 = int(datetime(2026, 10, 12, 19, 36, 45, tzinfo=timezone.utc).timestamp())
t_eval_00 = int(datetime(2026, 10, 12, 19, 36, 0, tzinfo=timezone.utc).timestamp())

dt = 15.0

print("=== TESTING HYPOTHESES FOR CASE 33 (END 19:35, EVAL 19:36) ===")

configs = [
    ("Hyp 1: seed=low(19:35:45)=30902.75, updates=19:36:00..19:36:45 (4 updates)",
     float(bars_15s[t_end_45]["low"]),
     [float(bars_15s[t]["close"]) for t in range(t_end_45 + 15, t_eval_45 + 1, 15)]),
     
    ("Hyp 2: seed=min_low(19:35)=30895.50, updates=19:36:00..19:36:45 (4 updates)",
     30895.50,
     [float(bars_15s[t]["close"]) for t in range(t_end_45 + 15, t_eval_45 + 1, 15)]),
     
    ("Hyp 3: seed=low(19:35:00)=30895.50, updates=19:35:15..19:36:45 (7 updates)",
     float(bars_15s[t_end_00]["low"]),
     [float(bars_15s[t]["close"]) for t in range(t_end_00 + 15, t_eval_45 + 1, 15)]),

    ("Hyp 4: seed=low(19:35:00)=30895.50, updates=19:35:00..19:36:45 (8 updates, including 19:35:00 close)",
     float(bars_15s[t_end_00]["low"]),
     [float(bars_15s[t]["close"]) for t in range(t_end_00, t_eval_45 + 1, 15)]),

    ("Hyp 5: seed=min_low(19:35)=30895.50, updates=19:35:15..19:36:45 (7 updates)",
     30895.50,
     [float(bars_15s[t]["close"]) for t in range(t_end_00 + 15, t_eval_45 + 1, 15)]),
]

for name, seed, closes in configs:
    print(f"\n--- {name} ---")
    print(f"Seed: {seed}, Number of closes: {len(closes)}")
    print(f"Closes: {closes}")
    solved_C = {}
    for lane, obs in obs_33.items():
        b0 = factors[lane]
        def sim(c_val):
            alpha = 2.0 / ((b0 * c_val / dt) + 1.0)
            st = seed
            for cl in closes:
                st += alpha * (cl - st)
            return st
        
        try:
            sol = brentq(lambda c: sim(c) - obs, 10.0, 1000.0)
            solved_C[lane] = sol
        except Exception as e:
            solved_C[lane] = None
            
    print("Solved C per lane:")
    for lane, sol in solved_C.items():
        if sol is not None:
            print(f"  {lane}: {sol:.4f} (round: {round(sol)})")
        else:
            print(f"  {lane}: No root found")
    valid_sols = [s for s in solved_C.values() if s is not None]
    if len(valid_sols) == 6:
        print(f"  Range of C: min={min(valid_sols):.4f}, max={max(valid_sols):.4f}, spread={max(valid_sols)-min(valid_sols):.4f}")
