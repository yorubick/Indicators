import json
from pathlib import Path

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

long_cases = [c for c in d["cases"] if c["branch"] == "long"]
print(f"Total long cases: {len(long_cases)}")

# Group by episode / day / hour
print(f"{'ID':32s} {'n':3s} {'C':6s} {'split':10s} {'START':16s} {'END':16s}")
for c in long_cases:
    st = c["START"][11:16]
    en = c["END"][11:16]
    print(f"{c['id']:32s} {c['bars']:3d} {c['C']:6.1f} {c['split']:10s} {st:16s} {en:16s}")
