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
t_e = time_map["19:30"]
t_eval = time_map["19:32"]

seed = float(rows[t_e]["low"])
print("Seed at END 19:30 (Low of 19:30):", seed)

dt = 60.0
factors = {
    "Lane 3 A": 24.0,
    "Lane 3 B": 89.0/3.0,
    "Lane 2 A": 8.0,
    "Lane 2 B": 89.0/9.0,
    "Lane 1 A": 72.0/27.0,
    "Lane 1 B": 89.0/27.0,
}

cands = [71, 88, 109, 130, 134, 135]
print("Candidates for START 19:03, END 19:30 on candle 19:32 UTC:")
print("C cand | Lane 3 A (Fast A) | Lane 2 A (Fast B) | Lane 1 A (Fast C)")
print("-" * 60)
for c in cands:
    sims = {}
    for lane, b0 in factors.items():
        alpha = 2.0 / ((b0 * float(c) / dt) + 1.0)
        st = seed
        for t in [time_map["19:31"], time_map["19:32"]]:
            cl = float(rows[t]["close"])
            st += alpha * (cl - st)
        sims[lane] = st
    v3 = sims["Lane 3 A"]
    v2 = sims["Lane 2 A"]
    v1 = sims["Lane 1 A"]
    print(f"{c:6d} | {v3:17.2f} | {v2:17.2f} | {v1:17.2f}")
