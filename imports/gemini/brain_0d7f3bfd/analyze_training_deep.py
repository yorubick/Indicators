import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"=== 32 TRAINING CASES ANALYSIS ===")
for i, c in enumerate(train):
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    opens = [b["open"] for b in ohlc]
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    closes = [b["close"] for b in ohlc]
    
    st = c["START"][11:16]
    en = c["END"][11:16]
    c_val = int(round(c["C"]))
    
    h_max = max(highs)
    l_min = min(lows)
    idx_max = highs.index(h_max)
    idx_min = lows.index(l_min)
    
    # Range
    rng = h_max - l_min
    
    print(f"[{i:2d}] {c['id']:28s} {st}->{en} dt={dt:3d} n={n:2d} C={c_val:3d} | H={h_max:.2f}(@{idx_max:2d}) L={l_min:.2f}(@{idx_min:2d}) Rng={rng:5.2f}")
