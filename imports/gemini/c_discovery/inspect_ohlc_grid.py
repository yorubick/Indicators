import csv
from datetime import datetime, timezone

bars_by_time = {}
with open(r"G:\trading\guias\analisis\manual\Lite_1904_193000_1m_b.csv", "r") as f:
    for r in csv.DictReader(f):
        t = int(r["time"])
        dt_val = datetime.fromtimestamp(t, tz=timezone.utc)
        if dt_val.strftime("%Y-%m-%d") == "2026-10-12":
            bars_by_time[t] = {
                "time": t,
                "open": float(r["open"]),
                "high": float(r["high"]),
                "low": float(r["low"]),
                "close": float(r["close"])
            }

times = sorted(bars_by_time.keys())
time_map = {datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"): t for t in times}

print("Time  | Open     | High     | Low      | Close")
print("-" * 50)
for m in ["19:20", "19:21", "19:22", "19:23", "19:24", "19:25", "19:26", "19:27", "19:28", "19:29", "19:30", "19:31", "19:32", "19:33", "19:34"]:
    t = time_map[m]
    b = bars_by_time[t]
    print(f"{m} | {b['open']:8.2f} | {b['high']:8.2f} | {b['low']:8.2f} | {b['close']:8.2f}")
