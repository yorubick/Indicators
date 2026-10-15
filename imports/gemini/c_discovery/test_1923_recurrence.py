import csv

csv_path = r"G:\trading\guias\analisis\manual\Lite_1903_192300_1m_b.csv"
rows = {}
with open(csv_path, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows[int(r["time"])] = r

t_end = 1791832980 # 19:23:00
t_1924 = 1791833040
t_1925 = 1791833100
t_1926 = 1791833160

# What was the seed?
# low of 19:23:00 is float(rows[t_end]["low"]) = 30864.25
seed = float(rows[t_end]["low"])
print(f"Seed (low of 19:23): {seed}")

# For Lane 3 A (base 24, C = 50, dt = 60)
C = 50.0
dt = 60.0
base = 24.0
alpha = 2.0 / (base * C / dt + 1.0) # 2 / (24 * 50 / 60 + 1) = 2 / (20 + 1) = 2/21 = 0.09523809523809523

print(f"Alpha: {alpha}")

# If recurrence updates on 19:24, 19:25, 19:26:
state = seed
for t in [t_1924, t_1925, t_1926]:
    close = float(rows[t]["close"])
    state += alpha * (close - state)
    print(f"Bar {t} (close={close}): state = {state}")

official_1926 = float(rows[t_1926]["Lane 3 A"])
print(f"Computed at 19:26: {state}")
print(f"Official at 19:26: {official_1926}")
print(f"Difference: {state - official_1926}")
