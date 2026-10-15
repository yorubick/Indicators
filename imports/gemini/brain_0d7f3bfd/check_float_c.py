import json

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

print("=== ALL FLOAT VALUES OF C IN DATASET ===")
for c in data['cases']:
    if c['bars'] >= 21:
        c_val = c['C']
        print(f"{c['id']}: bars={c['bars']}, dt={c['dt']}, C={c_val!r}, type={type(c_val).__name__}")
