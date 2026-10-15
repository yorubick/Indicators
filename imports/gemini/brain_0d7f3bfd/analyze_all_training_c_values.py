import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Loaded {len(train)} training cases.")

# Let's inspect each training case in detail:
# Look at the values of C:
# 16, 50, 52, 55, 60, 71, 73, 77, 80, 102, 109, 128, 134, 137

# Group training cases by their actual C value:
from collections import defaultdict
c_groups = defaultdict(list)
for c in train:
    c_groups[int(round(c["C"]))].append(c)

print("\nGrouped by C value:")
for c_val in sorted(c_groups.keys()):
    cases = c_groups[c_val]
    print(f"\n--- C = {c_val} ({len(cases)} cases) ---")
    for c in cases:
        st = c["START"][11:16]
        en = c["END"][11:16]
        dt = c["dt"]
        n = c["bars"]
        ohlc = c["OHLC"]
        highs = [b["high"] for b in ohlc]
        lows = [b["low"] for b in ohlc]
        rng = max(highs) - min(lows)
        i_max = highs.index(max(highs))
        i_min = lows.index(min(lows))
        print(f"  {c['id'][:26]} {st}->{en} dt={dt:3d} n={n:2d} | H={max(highs):.2f}(@{i_max:2d}) L={min(lows):.2f}(@{i_min:2d}) Rng={rng:5.2f}")
