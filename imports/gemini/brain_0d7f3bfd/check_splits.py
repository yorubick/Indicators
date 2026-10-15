import json
from pathlib import Path

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

long_cases = [c for c in d["cases"] if c["branch"] == "long"]
train = [c for c in long_cases if c["split"] == "training"]
val = [c for c in long_cases if c["split"] == "validation"]

print(f"Long training cases ({len(train)}):")
for c in train:
    st = c["START"][11:16]
    en = c["END"][11:16]
    print(f"  {c['id']:32s} {st}->{en} n={c['bars']:2d} C={c['C']:5.1f}")

print(f"\nLong validation cases ({len(val)}):")
for c in val:
    st = c["START"][11:16]
    en = c["END"][11:16]
    print(f"  {c['id']:32s} {st}->{en} n={c['bars']:2d} C={c['C']:5.1f}")
