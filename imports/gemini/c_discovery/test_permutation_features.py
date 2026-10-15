import json
import numpy as np

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = [c for c in d["cases"] if c.get("bars", 0) >= 21 and c.get("C_Lite") is not None]

# Extract permutation/time features for each case
X = []
Y = []
info = []

for c in cases:
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    c_val = c["C_Lite"]
    
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    
    # Argmax and argmin
    ih = highs.index(max(highs))
    il = lows.index(min(lows))
    
    # Distance between extremes
    d_hl = abs(ih - il)
    
    # First extreme and last extreme
    first_ext = min(ih, il)
    last_ext = max(ih, il)
    
    # Bars from start to first extreme, between extremes, from last extreme to end
    seg1 = first_ext
    seg2 = last_ext - first_ext
    seg3 = n - 1 - last_ext
    
    # Number of green bars
    n_green = sum(1 for b in ohlc if b["close"] > b["open"])
    
    X.append([
        n,
        dt,
        ih,
        il,
        d_hl,
        seg1,
        seg2,
        seg3,
        n_green,
        (n * dt) / 18.3
    ])
    Y.append(c_val)
    info.append((c["id"], c["START"], c["END"]))

X = np.array(X)
Y = np.array(Y)

print("Correlation with C:")
feature_names = ["n", "dt", "idx_high", "idx_low", "dist_HL", "seg_start", "seg_between", "seg_end", "n_green", "T/18.3"]
for j, name in enumerate(feature_names):
    corr = np.corrcoef(X[:, j], Y)[0, 1]
    print(f"  {name:12s}: corr = {corr:+.4f}")
