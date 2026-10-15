import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = d.get("cases", [])
matches = []
for c in cases:
    s = c.get("START", "")
    e = c.get("END", "")
    if ("19:03" in s or "19:04" in s) and "19:" in e and c.get("dt") == 60:
        matches.append(c)

print(f"Found {len(matches)} cases for START 19:03/04 (60s):")
for m in sorted(matches, key=lambda x: (x["START"], x["END"])):
    print(f"START: {m['START'][11:19]} | END: {m['END'][11:19]} | bars: {m['bars']:2d} | C_Lite: {m.get('C_Lite')}")
