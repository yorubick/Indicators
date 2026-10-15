import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Testing on {len(train)} training cases:")

# What exact deterministic rules map the OHLC of the 32 training cases to their target C?
# Let's inspect the target C values in training:
targets = [round(c["C"]) for c in train]
print("Distinct C in training:", sorted(set(targets)))

# For each case, look at:
# - start time, end time, n, dt
# - H, L, first O/H/L/C, last O/H/L/C
# - bar index of H, bar index of L
# - number of bars between H and L
# - distance from last extreme to END
