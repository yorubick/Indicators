# Calculate exact curve predictions for END 19:36 evaluated at 19:37
import csv
from datetime import datetime, timezone

with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

t_end_00 = int(datetime(2026, 10, 12, 19, 36, 0, tzinfo=timezone.utc).timestamp())
t_end_45 = t_end_00 + 45
t_eval_45 = int(datetime(2026, 10, 12, 19, 37, 45, tzinfo=timezone.utc).timestamp())

# Seed is 1m low of END bar (19:36)
seed = min(float(bars_15s[t]["low"]) for t in range(t_end_00, t_end_45 + 1, 15))

# Closes of eval candle (19:37)
closes = [float(bars_15s[t]["close"]) for t in range(t_end_45 + 15, t_eval_45 + 1, 15)]

factors = {
    "Lane 3 A": 24.0,           # Lane A Fast
    "Lane 3 B": 89.0 / 3.0,     # Lane A Slow
    "Lane 2 A": 8.0,            # Lane B Fast
    "Lane 2 B": 89.0 / 9.0,     # Lane B Slow
    "Lane 1 A": 72.0 / 27.0,    # Lane C Fast
    "Lane 1 B": 89.0 / 27.0,    # Lane C Slow
}

dt = 15.0

print(f"Seed for END 19:36: {seed}")
print(f"Closes for 19:37: {closes}")
print("\n=== PREDICCIÓN DE CURVAS OFICIALES PARA END = 19:36, EVAL = 19:37 ===")

for c_cand in [87, 88, 106, 112, 123]:
    print(f"\n--- Si C_15s = {c_cand} ---")
    for lane, b0 in factors.items():
        alpha = 2.0 / ((b0 * c_cand / dt) + 1.0)
        st = seed
        for cl in closes:
            st += alpha * (cl - st)
        print(f"  {lane:<9}: {st:.2f}")
