import json
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

cases_15 = [c for c in data['cases'] if c['START'].startswith('2026-10-12T15')]

table = {}
for c in cases_15:
    st = c['START'][11:16]
    en = c['END'][11:16]
    C = round(c['C'])
    bars = c['bars']
    table.setdefault(st, {})[en] = f"{C}(n={bars})"

df = pd.DataFrame(table).fillna("-")
print(df.to_string())
