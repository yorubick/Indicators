import json
from pathlib import Path

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"{'ID':28s} {'n':3s} {'C':4s} {'n_eff = C*61/(200*dt/60)':25s} {'diff = n - n_eff':18s}")
for c in train:
    dt = c["dt"]
    c_val = c["C"]
    n = c["bars"]
    # n_eff
    factor = (200.0 / 61.0) * (dt / 60.0)
    n_eff = c_val / factor
    diff = n - n_eff
    print(f"{c['id']:28s} {n:3d} {round(c_val):4d} {n_eff:10.3f} (round={round(n_eff):2d}) {diff:10.3f}")
