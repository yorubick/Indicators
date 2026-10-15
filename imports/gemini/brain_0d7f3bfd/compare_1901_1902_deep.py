import json, datetime
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

# Collect all cases with n=21 starting between 18:58 and 19:04
sub_cases = []
for c in d["cases"]:
    if c["dt"] == 60 and c["bars"] == 21:
        st = c["START"][11:16]
        if st in ["18:58", "18:59", "19:00", "19:01", "19:02", "19:03", "19:04"]:
            sub_cases.append(c)

print(f"Found {len(sub_cases)} cases with n=21:")
for c in sub_cases:
    st = c["START"][11:16]
    en = c["END"][11:16]
    ohlc = c["OHLC"]
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    closes = [b["close"] for b in ohlc]
    opens = [b["open"] for b in ohlc]
    
    # Check extremes
    h_max = max(highs)
    l_min = min(lows)
    i_max = highs.index(h_max)
    i_min = lows.index(l_min)
    
    print(f"[{st} - {en}] C={round(c['C']):2d} | H={h_max:.2f}(@{i_max:2d}) L={l_min:.2f}(@{i_min:2d}) | FirstBar: O={opens[0]:.2f} H={highs[0]:.2f} L={lows[0]:.2f} C={closes[0]:.2f} | LastBar: O={opens[-1]:.2f} H={highs[-1]:.2f} L={lows[-1]:.2f} C={closes[-1]:.2f}")
