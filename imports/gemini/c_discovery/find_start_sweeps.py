import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = d.get("cases", [])
# Find cases with END = 19:23:00 on 60s
end_1923_cases = [c for c in cases if "19:23" in c.get("END", "") and c.get("dt") == 60]
print(f"Cases with END 19:23 (60s): {len(end_1923_cases)}")
for c in end_1923_cases:
    print(f"START: {c.get('START')} | bars: {c.get('bars')} | C_Lite: {c.get('C_Lite')}")

# Find cases with END = 19:20:00 on 60s
end_1920_cases = [c for c in cases if "19:20" in c.get("END", "") and c.get("dt") == 60]
print(f"\nCases with END 19:20 (60s): {len(end_1920_cases)}")
for c in end_1920_cases:
    print(f"START: {c.get('START')} | bars: {c.get('bars')} | C_Lite: {c.get('C_Lite')}")
