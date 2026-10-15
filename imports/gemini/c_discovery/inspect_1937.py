import csv
from datetime import datetime, timezone

with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

t_37 = int(datetime(2026, 10, 12, 19, 37, 0, tzinfo=timezone.utc).timestamp())
for s in [0, 15, 30, 45]:
    t = t_37 + s
    b = bars_15s.get(t)
    if b:
        print(f"19:37:{s:02d} -> O={b['open']} H={b['high']} L={b['low']} C={b['close']}")
    else:
        print(f"19:37:{s:02d} -> missing")
