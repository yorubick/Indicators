import json

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

with open(r'G:\trading\guias\analisis\C_evolucion87_resultados.json') as f:
    data13 = json.load(f)

all_long_60 = [c for c in data['cases'] if c['bars'] >= 21 and c['dt'] == 60]
c_values_60 = set(round(c['C']) for c in all_long_60)
for c in data13['cases']:
    c_values_60.add(round(c['C']))

print("All distinct C values for dt=60 in dataset + Oct 13:")
c_sorted = sorted(list(c_values_60))
print(c_sorted)

print("\nChecking remainder modulo 3:")
for c in c_sorted:
    rem = c % 3
    div3 = c // 3
    print(f"C = {c:3d} | C / 60 = {c/60:6.3f} | C % 3 = {rem} (3 * {div3} + {rem})")
