import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

cases = master["cases"]
large_c = [c for c in cases if (c.get("C_Lite") or c.get("C") or 0) > 100]
print(f"Total cases with C > 100: {len(large_c)}")
for c in large_c:
    c_val = c.get("C_Lite") or c.get("C")
    dt = c["dt"]
    n = c["bars"]
    s = c["START"]
    e = c["END"]
    cid = c["id"]
    print(f"{cid:32} | dt:{dt:3d} | n:{n:3d} | C:{c_val:8.2f} | {s[11:19]} -> {e[11:19]}")
