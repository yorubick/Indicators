import json, math

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = master['cases']
lite_none = [c for c in cases if c['C_Lite'] is None]

all_single_int = True
for c in lite_none:
    low = c['C_Character_interval']['lower_inclusive']
    high = c['C_Character_interval']['upper_exclusive']
    ints = [i for i in range(math.floor(low), math.ceil(high) + 1) if low <= i < high]
    if len(ints) != 1:
        print(f"Mismatch for {c['id']}: {ints}")
        all_single_int = False

if all_single_int:
    print(f"All {len(lite_none)} Character-only cases have EXACTLY ONE unique integer in their interval!")
