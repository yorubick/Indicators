import json

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

long_cases = [c for c in data['cases'] if c['bars'] >= 21]

print("Case ID                     | n  | dt | C   | TimeSpan | TimeSpan / C | (n*dt) / C | C / dt")
print("-" * 85)
for c in sorted(long_cases, key=lambda x: (x['split'], x['START'], x['bars'])):
    n = c['bars']
    dt = c['dt']
    C = round(c['C'])
    t_span = (n - 1) * dt
    t_tot = n * dt
    m1 = t_span / C
    m2 = t_tot / C
    print(f"[{c['split'][:5]}] {c['START'][11:19]}->{c['END'][11:19]} | {n:2d} | {dt:2d} | {C:3d} | {t_span:8d} | {m1:12.4f} | {m2:10.4f} | {C/dt:6.3f}")
