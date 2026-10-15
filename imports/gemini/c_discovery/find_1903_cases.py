import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = d.get("cases", [])
print(f"Total cases: {len(cases)}")
for c in cases:
    s = c.get("START", "")
    e = c.get("END", "")
    if "19:03" in s:
        print(f"START: {s} | END: {e} | TF: {c.get('source_seconds')}s | bars: {c.get('bars')} | C_Lite: {c.get('C_Lite')}")
