import csv
from datetime import datetime, timezone

rows = {}
with open(r"G:\trading\guias\analisis\manual\Lite_1904_193000_1m_b.csv", "r") as f:
    for r in csv.DictReader(f):
        t = int(r["time"])
        dt_val = datetime.fromtimestamp(t, tz=timezone.utc)
        if dt_val.strftime("%Y-%m-%d") == "2026-10-12":
            rows[t] = r

sorted_times = sorted(rows.keys())
time_map = {datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"): t for t in sorted_times}

t_s = time_map["19:03"]
t_e = time_map["19:32"]

seed = float(rows[t_e]["low"]) # 30874.50
print("Seed at END 19:32 (Low of 19:32):", seed)

# Post end bars: 19:33, 19:34
for m in ["19:32", "19:33", "19:34"]:
    t = time_map[m]
    r = rows[t]
    print(f"{m}: O={r['open']} H={r['high']} L={r['low']} C={r['close']}")

dt = 60.0
factors = {
    "Lane 3 A": 24.0,
    "Lane 3 B": 89.0/3.0,
    "Lane 2 A": 8.0,
    "Lane 2 B": 89.0/9.0,
    "Lane 1 A": 72.0/27.0,
    "Lane 1 B": 89.0/27.0,
}

def sim(b0, c_val, eval_bars):
    alpha = 2.0 / ((b0 * c_val / dt) + 1.0)
    st = seed
    for t in eval_bars:
        cl = float(rows[t]["close"])
        st += alpha * (cl - st)
    return st

cands = [71, 88, 109, 112, 130, 135, 136]

print("\n--- SIMULATION ON CANDLE 19:33 UTC (1 bar post-END) ---")
print("C cand | Lane 3 A (Fast A) | Lane 2 A (Fast B) | Lane 1 A (Fast C)")
print("-" * 60)
for c in cands:
    v3 = sim(factors["Lane 3 A"], float(c), [time_map["19:33"]])
    v2 = sim(factors["Lane 2 A"], float(c), [time_map["19:33"]])
    v1 = sim(factors["Lane 1 A"], float(c), [time_map["19:33"]])
    print(f"{c:6d} | {v3:17.2f} | {v2:17.2f} | {v1:17.2f}")

print("\n--- SIMULATION ON CANDLE 19:34 UTC (2 bars post-END) ---")
print("C cand | Lane 3 A (Fast A) | Lane 2 A (Fast B) | Lane 1 A (Fast C)")
print("-" * 60)
for c in cands:
    v3 = sim(factors["Lane 3 A"], float(c), [time_map["19:33"], time_map["19:34"]])
    v2 = sim(factors["Lane 2 A"], float(c), [time_map["19:33"], time_map["19:34"]])
    v1 = sim(factors["Lane 1 A"], float(c), [time_map["19:33"], time_map["19:34"]])
    print(f"{c:6d} | {v3:17.2f} | {v2:17.2f} | {v1:17.2f}")
