import csv
from datetime import datetime, timezone

with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

for minute in [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]:
    t_min = int(datetime(2026, 10, 12, 19, minute, 0, tzinfo=timezone.utc).timestamp())
    print(f"=== Minute 19:{minute:02d} ===")
    for offset in [0, 15, 30, 45]:
        t = t_min + offset
        if t in bars_15s:
            b = bars_15s[t]
            dt_str = datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M:%S")
            print(f"  {dt_str}: O={b['open']} H={b['high']} L={b['low']} C={b['close']}")
        else:
            print(f"  {t}: missing")
