import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

# Find all cases with dt=60 and bars=21
cases_21 = [c for c in d["cases"] if c["dt"] == 60 and c["bars"] == 21]

print(f"Total cases with dt=60 and n=21: {len(cases_21)}")

rows = []
for c in cases_21:
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    opens = np.array([b["open"] for b in ohlc])
    highs = np.array([b["high"] for b in ohlc])
    lows = np.array([b["low"] for b in ohlc])
    closes = np.array([b["close"] for b in ohlc])
    
    h_max = np.max(highs)
    l_min = np.min(lows)
    i_max = int(np.argmax(highs))
    i_min = int(np.argmin(lows))
    
    rng = h_max - l_min
    tr = np.maximum(highs - lows, np.abs(highs - np.roll(closes, 1)))
    tr[0] = highs[0] - lows[0]
    atr = np.mean(tr)
    
    net_c = closes[-1] - closes[0]
    net_abs = abs(net_c)
    gross_path = np.sum(np.abs(np.diff(closes)))
    er = net_abs / gross_path if gross_path > 0 else 0
    
    first_body = closes[0] - opens[0]
    first_rng = highs[0] - lows[0]
    
    # Volume if present
    vol = np.sum([b.get("volume", 0) for b in ohlc])
    
    # Number of bars between extremes
    dist_hl = abs(i_max - i_min)
    
    st = c["START"][11:16]
    en = c["END"][11:16]
    c_val = int(round(c["C"]))
    
    rows.append({
        "id": c["id"][:26],
        "st_en": f"{st}-{en}",
        "C": c_val,
        "rng": rng,
        "atr": round(atr, 2),
        "er": round(er, 2),
        "dist_hl": dist_hl,
        "i_max": i_max,
        "i_min": i_min,
        "net_c": round(net_c, 2),
        "first_rng": round(first_rng, 2)
    })

import pandas as pd
df = pd.DataFrame(rows).sort_values("C")
print(df.to_string())
