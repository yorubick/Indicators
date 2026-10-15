import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = {c["id"]: c for c in d["cases"]}

# Let's find the case with C=62 -> 83 (bars 22->23, dt=60s)
for c in d["cases"]:
    if c.get("dt") == 60 and c.get("bars") in [22, 23] and c.get("C_Lite") is not None:
        if abs(c["C_Lite"] - 83.0) < 0.1 or abs(c["C_Lite"] - 62.0) < 0.1:
            print(f"Case {c['id'][:30]} | START={c['START'][11:19]} END={c['END'][11:19]} | bars={c['bars']} | C={c['C_Lite']}")

# Also find C=69 -> 93 (bars 24->25, dt=60s)
for c in d["cases"]:
    if c.get("dt") == 60 and c.get("bars") in [24, 25] and c.get("C_Lite") is not None:
        if abs(c["C_Lite"] - 93.0) < 0.1 or abs(c["C_Lite"] - 69.0) < 0.1:
            print(f"Case {c['id'][:30]} | START={c['START'][11:19]} END={c['END'][11:19]} | bars={c['bars']} | C={c['C_Lite']}")
