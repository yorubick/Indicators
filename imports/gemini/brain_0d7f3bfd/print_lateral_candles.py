import json, datetime
from pathlib import Path

p = Path("G:/trading/guias/analisis/C_START_regimenes.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

# Find case with regime lateral
for c in d["cases"]:
    if c["regime"] == "lateral" and c["bars"] == 24: # 06:57 to 07:20
        print(f"Candles in Lateral Case ({c['START']} - {c['END']}):")
        print(f"{'Time':6s} {'Open':9s} {'High':9s} {'Low':9s} {'Close':9s} {'Range':6s}")
        for b in c["OHLC"]:
            dt = datetime.datetime.fromtimestamp(b["time"], datetime.timezone.utc).strftime("%H:%M")
            o, h, l, cl = float(b["open"]), float(b["high"]), float(b["low"]), float(b["close"])
            print(f"{dt:6s} {o:9.2f} {h:9.2f} {l:9.2f} {cl:9.2f} {h-l:6.2f}")
        break
