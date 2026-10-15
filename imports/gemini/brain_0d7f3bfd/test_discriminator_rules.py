import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Loaded {len(train)} training cases.")

# We want to distinguish:
# Class 1: M = 24 (C = floor((n-1)*60/24) = 50, 52, 55, 60)
# Class 2: Breakout C = 71
# Class 3: Base C = 77
# Class 4: Spikes C in {102, 109, 128, 134, 137}
# Class 5: Others C in {16, 73, 80}

# Let's inspect features of the first 3 bars and the extremes:
for c in train:
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    c_val = int(round(c["C"]))
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    closes = [b["close"] for b in ohlc]
    opens = [b["open"] for b in ohlc]
    
    i_max = highs.index(max(highs))
    i_min = lows.index(min(lows))
    bs_max = n - 1 - i_max
    
    # First candle
    rng_0 = highs[0] - lows[0]
    
    # Range of first 3 bars
    rng_3 = max(highs[:3]) - min(lows[:3])
    
    # Total range
    rng_tot = max(highs) - min(lows)
    
    # Ratio
    ratio_0_tot = rng_0 / rng_tot
    ratio_3_tot = rng_3 / rng_tot
    
    st = c["START"][11:16]
    en = c["END"][11:16]
    
    print(f"[{st}-{en}] n={n:2d} dt={dt:3d} C={c_val:3d} | rng_0={rng_0:5.2f} rng_3={rng_3:5.2f} rng_tot={rng_tot:5.2f} r0={ratio_0_tot:.3f} r3={ratio_3_tot:.3f} | i_max={i_max:2d} i_min={i_min:2d} bs_max={bs_max:2d}")
