import csv
from datetime import datetime, timezone

with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Case: START 19:30, END 19:33, Eval 19:34
t_start = int(datetime(2026, 10, 12, 19, 30, 0, tzinfo=timezone.utc).timestamp())
t_end_00 = int(datetime(2026, 10, 12, 19, 33, 0, tzinfo=timezone.utc).timestamp())
t_end_45 = t_end_00 + 45
t_eval_45 = int(datetime(2026, 10, 12, 19, 34, 45, tzinfo=timezone.utc).timestamp())

seed = min(float(bars_15s[t]["low"]) for t in range(t_end_00, t_end_45 + 1, 15))
closes_34 = [float(bars_15s[t]["close"]) for t in range(t_end_45 + 15, t_eval_45 + 1, 15)]

factors = {
    "Lane 3 A": 24.0,           # Lane A Fast
    "Lane 3 B": 89.0 / 3.0,     # Lane A Slow
    "Lane 2 A": 8.0,            # Lane B Fast
    "Lane 2 B": 89.0 / 9.0,     # Lane B Slow
    "Lane 1 A": 72.0 / 27.0,    # Lane C Fast
    "Lane 1 B": 89.0 / 27.0,    # Lane C Slow
}

dt = 15.0

print("\n=== TABLA DE PREDICCIONES TEÓRICAS (START 19:30, END 19:33, EVAL 19:34) ===")
print(f"{'C (s)':<6} | {'Lane 1 A':<10} | {'Lane 1 B':<10} | {'Lane 2 A':<10} | {'Lane 2 B':<10} | {'Lane 3 A':<10} | {'Lane 3 B':<10}")
print("-" * 76)

candidates = [9, 10, 12, 15, 16]
for c_cand in candidates:
    res = {}
    for lane, b0 in factors.items():
        alpha = 2.0 / ((b0 * c_cand / dt) + 1.0)
        st = seed
        for cl in closes_34:
            st += alpha * (cl - st)
        res[lane] = st
    print(f"{c_cand:<6} | {res['Lane 1 A']:<10.2f} | {res['Lane 1 B']:<10.2f} | {res['Lane 2 A']:<10.2f} | {res['Lane 2 B']:<10.2f} | {res['Lane 3 A']:<10.2f} | {res['Lane 3 B']:<10.2f}")
