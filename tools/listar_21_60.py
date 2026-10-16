import json

master = json.load(open('master_all_C_cases.json'))
cases = [c for c in master['cases'] if c.get('bars') == 21 and c.get('dt') == 60 and c.get('C_Lite') is not None]

print(f"Total cases with bars=21, dt=60s: {len(cases)}")
for c in cases:
    s = c['START'][11:19]
    e = c['END'][11:19]
    print(f"{c['id']}: START={s}, END={e}, C={c['C_Lite']:.1f}")
