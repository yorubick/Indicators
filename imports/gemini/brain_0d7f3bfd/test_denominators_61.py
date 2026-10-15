import json
from pathlib import Path

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print("Analyzing C * 61 / n for each training case:")
for c in train:
    n = c["bars"]
    dt = c["dt"]
    c_val = c["C"]
    
    # If dt == 60:
    # C = round( n * K / 61 )
    # What is K = C * 61 / n ?
    if dt == 60:
        k = c_val * 61.0 / n
        print(f"{c['id']:28s} n={n:2d} C={round(c_val):3d} -> K = {k:7.3f} (round K = {round(k):3d})")
