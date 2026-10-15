import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Testing discriminator on {len(train)} training cases:")

for c in train:
    if c["dt"] == 60:
        ohlc = c["OHLC"]
        n = len(ohlc)
        c_val = int(round(c["C"]))
        highs = [b["high"] for b in ohlc]
        lows = [b["low"] for b in ohlc]
        
        i_max = highs.index(max(highs))
        i_min = lows.index(min(lows))
        first_ext = min(i_max, i_min)
        
        rng_3 = max(highs[:3]) - min(lows[:3])
        rng_tot = max(highs) - min(lows)
        r3 = rng_3 / rng_tot
        
        # Test classifier:
        # If first_ext <= 2 or r3 >= 0.50 -> Base State
        # Else -> Consolidation / Breakout State
        is_base = (first_ext <= 2 or r3 >= 0.50)
        
        st = c["START"][11:16]
        en = c["END"][11:16]
        print(f"[{st}-{en}] n={n:2d} C={c_val:3d} | first_ext={first_ext:2d} r3={r3:.3f} -> Predicted: {'BASE' if is_base else 'INTERIOR'}")
