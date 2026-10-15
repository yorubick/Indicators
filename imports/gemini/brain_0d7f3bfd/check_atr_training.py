import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

long_cases = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Analyzing {len(long_cases)} training cases:")
print(f"{'ID':30s} {'n':3s} {'C':5s} {'Rng':7s} {'ATR':6s} {'Rng/ATR':8s} {'SumTR':8s}")

for c in long_cases:
    ohlc = c["OHLC"]
    highs = np.array([b["high"] for b in ohlc])
    lows = np.array([b["low"] for b in ohlc])
    closes = np.array([b["close"] for b in ohlc])
    rng = max(highs) - min(lows)
    
    # TR calculation
    tr = np.zeros(len(ohlc))
    tr[0] = highs[0] - lows[0]
    for i in range(1, len(ohlc)):
        tr[i] = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
    atr = np.mean(tr)
    sum_tr = np.sum(tr)
    ratio = rng / atr if atr > 0 else 0
    print(f"{c['id']:30s} {c['bars']:3d} {int(c['C']):5d} {rng:7.2f} {atr:6.2f} {ratio:8.2f} {sum_tr:8.2f}")
