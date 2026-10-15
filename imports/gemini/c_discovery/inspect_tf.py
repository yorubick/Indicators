import json

with open(r"G:\trading\guias\analisis\C_test_timeframes_1900_1920.json", "r", encoding="utf-8") as f:
    tf = json.load(f)

print(json.dumps(tf, indent=2))
