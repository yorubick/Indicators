import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

cases = master["cases"]
long_cases = [c for c in cases if c.get("bars") >= 21]

non_integers = []
for c in long_cases:
    cl = c.get("C_Lite")
    if cl is not None:
        diff_from_int = abs(cl - round(cl))
        if diff_from_int > 1e-4:
            non_integers.append((c["id"], c["bars"], c["dt"], cl, diff_from_int))

print(f"Long cases with C_Lite: {len([c for c in long_cases if c.get('C_Lite') is not None])}")
print(f"Non-integer C_Lite in long regime: {len(non_integers)}")
for item in non_integers:
    print("  ", item)
