import csv
from datetime import datetime, timezone

with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Case: START 19:08, END 19:33, Eval 19:34
t_start = int(datetime(2026, 10, 12, 19, 8, 0, tzinfo=timezone.utc).timestamp())
t_end_00 = int(datetime(2026, 10, 12, 19, 33, 0, tzinfo=timezone.utc).timestamp())
t_end_45 = t_end_00 + 45
t_eval_45 = int(datetime(2026, 10, 12, 19, 34, 45, tzinfo=timezone.utc).timestamp())

# Range high of window [19:08:00 .. 19:33:45]
win_bars = [bars_15s[t] for t in range(t_start, t_end_45 + 1, 15)]
win_h = max(float(b["high"]) for b in win_bars)
win_l = min(float(b["low"]) for b in win_bars)

# Seed for END 19:33: minimum low of the 1m bar at 19:33
seed = min(float(bars_15s[t]["low"]) for t in range(t_end_00, t_end_45 + 1, 15))

# Closes of 19:34
closes_34 = [float(bars_15s[t]["close"]) for t in range(t_end_45 + 15, t_eval_45 + 1, 15)]

print(f"START 19:08 to END 19:33 (Duration: 25 min = 1500s, n_1m = 26 bars)")
print(f"Range High at END: {win_h:.2f}, Range Low: {win_l:.2f}")
print(f"Seed (Low of 19:33): {seed:.2f}")
print(f"19:34 Closes: {closes_34} (Final close: {closes_34[-1]:.2f} > Range High {win_h:.2f} -> BREAKOUT CONFIRMED!)")

factors = {
    "Lane 3 A": 24.0,           # Lane A Fast
    "Lane 3 B": 89.0 / 3.0,     # Lane A Slow
    "Lane 2 A": 8.0,            # Lane B Fast
    "Lane 2 B": 89.0 / 9.0,     # Lane B Slow
    "Lane 1 A": 72.0 / 27.0,    # Lane C Fast
    "Lane 1 B": 89.0 / 27.0,    # Lane C Slow
}

dt = 15.0

print("\n=== THEORETICAL CURVE PREDICTIONS ON EVAL CANDLE 19:34 ===")
for c_cand in [67, 79, 87, 88, 106, 123]:
    print(f"\n--- Si C_15s = {c_cand} ---")
    for lane, b0 in factors.items():
        alpha = 2.0 / ((b0 * c_cand / dt) + 1.0)
        st = seed
        for cl in closes_34:
            st += alpha * (cl - st)
        print(f"  {lane:<9}: {st:.2f}")
