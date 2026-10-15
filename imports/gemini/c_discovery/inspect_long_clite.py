import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

cases = master["cases"]
long_cases = [c for c in cases if c.get("bars") >= 21]

print("Long cases C_Lite samples:")
for c in long_cases[:30]:
    cl = c.get("C_Lite")
    c_int = c.get("C")
    kind = c.get("C_measurement_kind")
    print(f"ID: {c['id']:35s} dt: {c['dt']:3d} bars: {c['bars']:3d} C: {c_int} C_Lite: {cl} kind: {kind}")
