import json

# Let's inspect all measured values of C in the dataset:
with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

long_cases = [c for c in data['cases'] if c['bars'] >= 21]
c_values = sorted(list(set(round(c['C']) for c in long_cases)))
print("Distinct long C values in dataset:", c_values)

# Let's list occurrences of each C:
for c_val in c_values:
    cases = [c for c in long_cases if round(c['C']) == c_val]
    splits = set(c['split'] for c in cases)
    dts = set(c['dt'] for c in cases)
    print(f"C = {c_val:3d} (x{len(cases):2d}): splits={splits}, dt={dts}")
