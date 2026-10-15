import json

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

# Find any case covering 18:54
for c in data['cases']:
    if '1858' in c['id'] or '1859' in c['id'] or '1900' in c['id']:
        print(f"Case: {c['id']}")

# Also let's check G:\trading\guias\analisis\C_barrido_15s_start1854_estabilizado.csv
import csv
with open(r'G:\trading\guias\analisis\C_barrido_15s_start1854_estabilizado.csv', encoding='utf-8-sig') as f:
    r = csv.DictReader(f)
    rows = list(r)
    print("CSV total rows:", len(rows))
    print("First row:", rows[0])
