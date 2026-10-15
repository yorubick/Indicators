import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

cases_15s = [c for c in master["cases"] if c.get("dt") == 15 and c.get("bars") >= 21]

print("15s cases (dt = 15):")
for c in cases_15s:
    c_val = c.get("C_Lite") or c.get("C")
    n = c["bars"]
    r24 = c_val / 0.625
    r8 = c_val / 1.875
    cid = c["id"]
    print(f"{cid:32} | n={n:3d} | C={c_val:6.2f} | C/0.625={r24:6.2f} | C/1.875={r8:6.2f}")
