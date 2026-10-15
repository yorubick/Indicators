import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Testing M = (n - 1) * dt / C across training cases:")

for c in train:
    n = c["bars"]
    dt = c["dt"]
    c_val = c["C"]
    t_span = (n - 1) * dt
    m = t_span / c_val
    print(f"{c['id']:28s} n={n:2d} dt={dt:3d} C={round(c_val):3d} -> M = t_span/C = {m:7.3f} (round M = {round(m):2d})")
