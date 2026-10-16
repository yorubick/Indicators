import json

data = json.load(open('master_all_C_cases.json'))
cases = data['cases']

print("Buscando casos con C cercano a 191, 195, 227:")
for c in cases:
    c_val = c['C']
    if any(abs(c_val - target) < 1.0 for target in [128, 177, 181, 190, 191, 195, 227]):
        print(f"ID: {c['id']}, bars: {c['bars']}, dt: {c['dt']}, C: {c_val}")
