import json
from pathlib import Path

# Load candles from C_matriz.json
p = Path("G:/trading/guias/analisis/C_matriz.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

# Extract OHLC for candles between 19:00 and 19:30
candles = {}
for c in d["cases"]:
    for b in c.get("OHLC", []):
        t = b["time"]
        candles[t] = b

import datetime
sorted_times = sorted(candles.keys())

print(f"{'Time':6s} {'Open':9s} {'High':9s} {'Low':9s} {'Close':9s} {'Rng':6s} {'Body':6s}")
for t in sorted_times:
    try:
        t_int = int(float(t))
        dt_str = datetime.datetime.fromtimestamp(t_int, datetime.timezone.utc).strftime("%H:%M")
    except:
        dt_str = str(t)
    o, h, l, c = float(b["open"]), float(b["high"]), float(b["low"]), float(b["close"])
    rng = h - l
    body = c - o
    print(f"{dt_str:6s} {o:9.2f} {h:9.2f} {l:9.2f} {c:9.2f} {rng:6.2f} {body:6.2f}")
