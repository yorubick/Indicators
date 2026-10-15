import json, datetime
from pathlib import Path

p = Path("G:/trading/guias/analisis/C_matriz.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

# Use case 23 (19:04 to 19:30) which contains all candles up to 19:30
c23 = d["cases"][23]
print(f"Candles in Case 23 ({c23['START']} - {c23['END']}):")
print(f"{'Time':6s} {'Open':9s} {'High':9s} {'Low':9s} {'Close':9s} {'Range':6s}")
for b in c23["OHLC"]:
    dt = datetime.datetime.fromtimestamp(int(b["time"]), datetime.timezone.utc).strftime("%H:%M")
    o, h, l, cl = float(b["open"]), float(b["high"]), float(b["low"]), float(b["close"])
    print(f"{dt:6s} {o:9.2f} {h:9.2f} {l:9.2f} {cl:9.2f} {h-l:6.2f}")
