import json, datetime
from pathlib import Path

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

# Find case 19:00 to 19:24
c = [x for x in d["cases"] if x["id"] == "20261012_190000_192400_60s"][0]
ohlc = c["OHLC"]

print(f"{'Idx':3s} {'Time':6s} {'Open':9s} {'High':9s} {'Low':9s} {'Close':9s} {'Range':6s} {'Body':6s}")
for i in range(12):
    b = ohlc[i]
    dt = datetime.datetime.fromtimestamp(b["time"], datetime.timezone.utc).strftime("%H:%M")
    o, h, l, cl = b["open"], b["high"], b["low"], b["close"]
    print(f"[{i:2d}] {dt:6s} {o:9.2f} {h:9.2f} {l:9.2f} {cl:9.2f} {h-l:6.2f} {cl-o:6.2f}")
