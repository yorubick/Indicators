import json
from pathlib import Path

# Load all candles from 15:26 to 15:52
path_23 = Path("G:/trading/guias/analisis/C_23_desplazamientos.json")
with open(path_23, "r", encoding="utf-8") as f:
    d23 = json.load(f)

# Collect all distinct candles
all_bars = {}
for c in d23["cases"]:
    for b in c["OHLC"]:
        all_bars[b["time"]] = b

sorted_times = sorted(all_bars.keys())
import datetime

print(f"{'Time UTC':10s} {'Open':10s} {'High':10s} {'Low':10s} {'Close':10s} {'Range':8s} {'Body':8s}")
for t in sorted_times:
    b = all_bars[t]
    dt_str = datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%H:%M")
    rng = b["high"] - b["low"]
    body = b["close"] - b["open"]
    print(f"{dt_str:10s} {b['open']:10.2f} {b['high']:10.2f} {b['low']:10.2f} {b['close']:10.2f} {rng:8.2f} {body:8.2f}")
