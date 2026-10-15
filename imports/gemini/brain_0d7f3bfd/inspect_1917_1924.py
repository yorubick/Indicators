import json, datetime
from pathlib import Path

p = Path("G:/trading/guias/analisis/C_matriz.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

# Find case 19:00 to 19:24
c = [x for x in d["cases"] if x["START"] == "19:00:00" and x["END"] == "19:24:00"][0]
ohlc = c["OHLC"]

print(f"{'Time':6s} {'Open':9s} {'High':9s} {'Low':9s} {'Close':9s} {'Rng':6s} {'Body':6s}")
for b in ohlc[17:]:
    dt = datetime.datetime.fromtimestamp(int(b["time"]), datetime.timezone.utc).strftime("%H:%M")
    o, h, l, cl = float(b["open"]), float(b["high"]), float(b["low"]), float(b["close"])
    print(f"{dt:6s} {o:9.2f} {h:9.2f} {l:9.2f} {cl:9.2f} {h-l:6.2f} {cl-o:6.2f}")
