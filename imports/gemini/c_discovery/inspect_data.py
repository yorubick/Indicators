import json
import os

with open(r"G:\trading\guias\analisis\master_all_C_cases_index.json", "r", encoding="utf-8") as f:
    index_data = json.load(f)

print(f"Index keys: {list(index_data.keys()) if isinstance(index_data, dict) else len(index_data)}")
if isinstance(index_data, list):
    print("First item in index:")
    print(json.dumps(index_data[0], indent=2))
elif isinstance(index_data, dict):
    first_k = list(index_data.keys())[0]
    print(f"Sample key: {first_k}")
    print(json.dumps(index_data[first_k], indent=2))

with open(r"G:\trading\guias\analisis\C_barrido_END_1855_1920_1924_15s.json", "r", encoding="utf-8") as f:
    barrido = json.load(f)

print(f"\nBarrido keys: {list(barrido.keys()) if isinstance(barrido, dict) else len(barrido)}")
if isinstance(barrido, dict):
    for k in list(barrido.keys())[:3]:
        print(f"Key: {k}")
        print(barrido[k].keys() if isinstance(barrido[k], dict) else type(barrido[k]))

with open(r"G:\trading\guias\analisis\C_test_timeframes_1900_1920.json", "r", encoding="utf-8") as f:
    tf_test = json.load(f)

print(f"\nTimeframe test keys: {list(tf_test.keys()) if isinstance(tf_test, dict) else len(tf_test)}")
