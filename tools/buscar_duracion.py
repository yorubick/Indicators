import json

master = json.load(open('master_all_C_cases.json'))
cases = master['cases']

print('Searching for cases with T ~ 2880s (48 min) in master:')
for c in cases:
    s = c.get('START')
    e = c.get('END')
    dt = c.get('dt')
    bars = c.get('bars')
    c_val = c.get('C_Lite') or c.get('C')
    
    t_inc = bars * dt if bars and dt else 0
    t_elap = (bars - 1) * dt if bars and dt else 0
    if abs(t_inc - 2880) <= 240 or abs(t_elap - 2880) <= 240:
        print(f"{c['id']}: dt={dt}, bars={bars}, t_inc={t_inc}, t_elap={t_elap}, C={c_val}")
