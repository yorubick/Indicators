import csv

csv_path = r"G:\trading\guias\analisis\manual\Lite_1903_192300_1m_b.csv"
rows = {}
with open(csv_path, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows[int(r["time"])] = r

target = 30867.31
alpha = 2.0 / (24.0 * 50.0 / 60.0 + 1.0) # 2/21 = 0.09523809523809523

# Let's test various possible seeds and start bars:
# Bar timestamps:
# 19:20: 1791832800
# 19:21: 1791832860
# 19:22: 1791832920
# 19:23: 1791832980
# 19:24: 1791833040
# 19:25: 1791833100
# 19:26: 1791833160

# What if seed was low of 19:22? (30866.75)
# What if seed was low of 19:20? (30866.5)
# What if it updated on 19:26 with 1 bar, 2 bars, 3 bars?
all_times = sorted(rows.keys())

for start_t in all_times:
    if 1791832500 <= start_t <= 1791833160:
        row = rows[start_t]
        for seed_name, seed_val in [("low", float(row["low"])), ("high", float(row["high"])), ("close", float(row["close"])), ("open", float(row["open"]))]:
            state = seed_val
            # Update for bars after start_t up to 19:26
            update_bars = [t for t in all_times if start_t < t <= 1791833160]
            for ub in update_bars:
                state += alpha * (float(rows[ub]["close"]) - state)
            if abs(state - target) < 0.1:
                print(f"MATCH! Start bar: {row['time']} ({seed_name}={seed_val}), Updated {len(update_bars)} bars -> state={state:.4f}")
