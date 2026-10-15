import csv
from datetime import datetime, timezone

with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Print 15s sub-bars with details: range, body, direction, wicks
print(f"{'Time':<8} | {'Type':<6} | {'Open':>9} | {'High':>9} | {'Low':>9} | {'Close':>9} | {'Rng':>5} | {'Body':>6} | {'UWick':>5} | {'LWick':>5}")
print("-" * 85)

for m in range(26, 36):
    t_min = int(datetime(2026, 10, 12, 19, m, 0, tzinfo=timezone.utc).timestamp())
    minute_type = "PEAK" if m in [26, 27, 29, 31, 34] else "TROUGH"
    print(f"=== 19:{m:02d} ({minute_type} in 1m) ===")
    for sec in [0, 15, 30, 45]:
        t = t_min + sec
        b = bars_15s[t]
        o, h, l, c = float(b["open"]), float(b["high"]), float(b["low"]), float(b["close"])
        rng = h - l
        body = c - o
        uwick = h - max(o, c)
        lwick = min(o, c) - l
        dt_str = datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M:%S")
        print(f"{dt_str:<8} | {'Up' if body>0 else 'Dn':<6} | {o:>9.2f} | {h:>9.2f} | {l:>9.2f} | {c:>9.2f} | {rng:>5.2f} | {body:>+6.2f} | {uwick:>5.2f} | {lwick:>5.2f}")
