import json
import pandas as pd

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases_15s = [c for c in master['cases'] if c['dt'] == 15]
print(f"Total 15s cases: {len(cases_15s)}")

rows = []
for c in cases_15s:
    start = c['START'].split('T')[1][:8]
    end = c['END'].split('T')[1][:8]
    c_val = c.get('C_Lite')
    if c_val is None:
        c_val = round(c['C_Character_interval']['lower_inclusive'])
    rows.append({
        'id': c['id'],
        'START': start,
        'END': end,
        'bars': c['bars'],
        'C': round(c_val, 2),
        'end_sec': int(end.split(':')[2]),
        'start_sec': int(start.split(':')[2])
    })

df = pd.DataFrame(rows)
df = df.sort_values(by=['START', 'END'])
print(df.to_string(index=False))
