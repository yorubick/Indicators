import json
import numpy as np

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

cases_21 = [c for c in data['cases'] if c['bars'] == 21 and c['dt'] == 60]

print("Case ID | Actual C | TimeSpan/M | What M gives exact C?")
print("-" * 65)
for c in sorted(cases_21, key=lambda x: round(x['C'])):
    C = round(c['C'])
    t_span = (21 - 1) * 60 # 1200 seconds
    t_tot = 21 * 60 # 1260 seconds
    
    m_span = t_span / C
    m_tot = t_tot / C
    
    print(f"[{c['split'][:5]}] {c['START'][11:16]}->{c['END'][11:16]} | C={C:2d} | 1200/C={m_span:6.3f} | 1260/C={m_tot:6.3f}")
