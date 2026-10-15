import json

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = master['cases']

cases_1923 = [c for c in cases if '1923' in c.get('END', '')]
print(f"Total cases with 1923 in END: {len(cases_1923)}")
for c in cases_1923:
    cid = c['id']
    dt = c['dt']
    bars = c['bars']
    c_lite = c.get('C_Lite')
    start = c['START'].split('T')[1][:8]
    end = c['END'].split('T')[1][:8]
    print(f"{cid:35s} | dt={dt:2d} | bars={bars:3d} | {start} -> {end} | C_Lite={c_lite}")
