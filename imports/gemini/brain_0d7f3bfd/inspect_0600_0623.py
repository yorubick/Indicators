import json, datetime
from pathlib import Path

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

c3 = [x for x in d["cases"] if x["id"] == "20261012_060000_062300_60s"][0]
ohlc = c3["OHLC"]

print("Candles 06:18 to 06:23:")
for i in range(18, len(ohlc)):
    b = ohlc[i]
    dt = datetime.datetime.fromtimestamp(b["time"], datetime.timezone.utc).strftime("%H:%M")
    print(f"[{i:2d}] {dt} O={b['open']:.2f} H={b['high']:.2f} L={b['low']:.2f} C={b['close']:.2f}")
