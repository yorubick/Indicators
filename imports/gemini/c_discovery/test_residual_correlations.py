import json
import numpy as np

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = [c for c in d["cases"] if c.get("bars", 0) >= 21 and c.get("C_Lite") is not None]

# Check correlations with the residual
residuals = []
features = []

for c in cases:
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    c_val = c["C_Lite"]
    res = c_val - (n * dt) / 18.3
    residuals.append(res)
    
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    closes = [b["close"] for b in ohlc]
    opens = [b["open"] for b in ohlc]
    
    ih = highs.index(max(highs))
    il = lows.index(min(lows))
    
    # Range efficiency: abs(close[-1] - open[0]) / sum(abs(close[i] - close[i-1]))
    path = sum(abs(closes[i] - closes[i-1]) for i in range(1, n))
    net = abs(closes[-1] - opens[0])
    eff = net / path if path > 0 else 0
    
    # Internal swings count
    swings = 0
    for i in range(1, n - 1):
        if (highs[i] > highs[i-1] and highs[i] > highs[i+1]) or (lows[i] < lows[i-1] and lows[i] < lows[i+1]):
            swings += 1
            
    # Position of close in range
    rng = max(highs) - min(lows)
    pos_close = (closes[-1] - min(lows)) / rng if rng > 0 else 0.5
    
    features.append([
        n,
        dt,
        ih / n,
        il / n,
        abs(ih - il) / n,
        eff,
        swings,
        pos_close,
        swings / n
    ])

features = np.array(features)
residuals = np.array(residuals)

names = ["n", "dt", "rel_idx_high", "rel_idx_low", "rel_dist_HL", "efficiency", "swings_count", "pos_close", "swing_freq"]
print("Correlation with Residual (C - T/18.3):")
for j, name in enumerate(names):
    corr = np.corrcoef(features[:, j], residuals)[0, 1]
    print(f"  {name:15s}: corr = {corr:+.4f}")
