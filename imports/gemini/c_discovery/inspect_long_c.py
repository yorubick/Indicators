import json
import numpy as np

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

cases = master["cases"]
long_cases = [c for c in cases if c.get("bars") >= 21]

print(f"Total long cases: {len(long_cases)}")
# Check unique C values in long cases
c_vals = sorted(list(set(c["C"] for c in long_cases)))
print(f"Unique C values in long cases ({len(c_vals)}):")
for v in c_vals:
    # count how many cases have this C
    cnt = sum(1 for c in long_cases if c["C"] == v)
    print(f"  C = {v:12.6f} (count = {cnt})")
