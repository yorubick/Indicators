import csv
from datetime import datetime, timezone

rows = []
with open(r"G:\trading\guias\analisis\manual\Lite_20261013_1900_1920_1m_a.csv", "r") as f:
    for r in csv.DictReader(f):
        t = int(r["time"])
        dt_val = datetime.fromtimestamp(t, tz=timezone.utc)
        if dt_val.strftime("%Y-%m-%d") == "2026-10-13":
            rows.append({
                "time": t,
                "time_str": dt_val.strftime("%H:%M"),
                "open": float(r["open"]),
                "high": float(r["high"]),
                "low": float(r["low"]),
                "close": float(r["close"])
            })

print(f"Total bars on 2026-10-13: {len(rows)}")
for r in rows:
    if "18:55" <= r["time_str"] <= "19:30":
        print(f"{r['time_str']} | O={r['open']:8.2f} H={r['high']:8.2f} L={r['low']:8.2f} C={r['close']:8.2f}")
