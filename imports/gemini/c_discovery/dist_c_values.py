import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

# Let's inspect all cases where C in long regime is measured
cases = [c for c in d["cases"] if c.get("bars", 0) >= 21 and c.get("C_Lite") is not None]

# Check the distribution of C_Lite values themselves!
from collections import Counter
c_integers = [round(c["C_Lite"]) for c in cases]
c_dist = Counter(c_integers)

print(f"Total unique C values across 110 cases: {len(c_dist)}")
print("Distribution of C values (sorted by frequency):")
for val, count in c_dist.most_common(20):
    print(f"  C = {val:3d} : {count:2d} cases ({count/len(cases)*100:.1f}%)")
