import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print("Case ID                       n   C   K=C*61/n   Rng   ATR   Rng/ATR   dist_HL  max_idx  min_idx")
for c in train:
    if c["dt"] == 60:
        n = c["bars"]
        c_val = c["C"]
        k = c_val * 61.0 / n
        ohlc = c["OHLC"]
        highs = [b["high"] for b in ohlc]
        lows = [b["low"] for b in ohlc]
        closes = [b["close"] for b in ohlc]
        rng = max(highs) - min(lows)
        tr = [highs[0]-lows[0]] + [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, n)]
        atr = np.mean(tr)
        i_max = highs.index(max(highs))
        i_min = lows.index(min(lows))
        d_hl = abs(i_max - i_min)
        print(f"{c['id']:28s} {n:2d} {round(c_val):3d} {k:8.2f} {rng:6.2f} {atr:5.2f} {rng/atr:7.2f} {d_hl:7d} {i_max:8d} {i_min:8d}")
