import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

cases = d["cases"]
print(f"Total cases: {len(cases)}")

# Let's see: for each case, find whether the extreme (max or min depending on trend) is at END, or interior:
rows = []
for c in cases:
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    closes = [b["close"] for b in ohlc]
    
    i_max = int(np.argmax(highs))
    i_min = int(np.argmin(lows))
    
    # Is max at last bar?
    max_at_end = (i_max == n - 1)
    min_at_end = (i_min == n - 1)
    
    # Distance from max to end, min to end
    dist_max_end = n - 1 - i_max
    dist_min_end = n - 1 - i_min
    
    rows.append({
        "id": c["id"],
        "branch": c["branch"],
        "split": c["split"],
        "n": n,
        "dt": dt,
        "C": round(c["C"], 2),
        "i_max": i_max,
        "i_min": i_min,
        "dist_max_end": dist_max_end,
        "dist_min_end": dist_min_end,
        "max_at_end": max_at_end,
        "min_at_end": min_at_end
    })

import pandas as pd
df = pd.DataFrame(rows)

# Filter to long branch
df_long = df[df["branch"] == "long"]
print("\nLong branch cases sorted by id:")
print(df_long[["id", "split", "n", "C", "dist_max_end", "dist_min_end"]].to_string())
