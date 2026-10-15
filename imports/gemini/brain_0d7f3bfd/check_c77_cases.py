import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

c77_cases = [c for c in d["cases"] if round(c["C"]) == 77 and c["dt"] == 60]
print(f"Total cases with C = 77: {len(c77_cases)}")

for c in c77_cases:
    ohlc = c["OHLC"]
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    n = len(ohlc)
    i_max = highs.index(max(highs))
    i_min = lows.index(min(lows))
    rng = max(highs) - min(lows)
    st = c["START"][11:16]
    en = c["END"][11:16]
    print(f"[{st} - {en}] n={n:2d} | H={max(highs):.2f}(@{i_max:2d}) L={min(lows):.2f}(@{i_min:2d}) Rng={rng:5.2f} | dist_HL={abs(i_max-i_min):2d}")
