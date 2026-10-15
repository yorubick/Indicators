import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

cases = master["cases"]
long_cases = [c for c in cases if c.get("bars") >= 21 and c.get("C_Lite") is not None]

diffs = [abs(c["C_Lite"] - round(c["C_Lite"])) for c in long_cases]
print("Max diff from integer among all 110 long cases:", max(diffs))
print("Min diff from integer among all 110 long cases:", min(diffs))
