import json

with open(r"G:\trading\guias\analisis\C_suficiencia_estado.json", "r", encoding="utf-8") as f:
    d = json.load(f)

for r in d["results"]:
    print(f"{r['signature']:35s} | collisions: {r['contradictory_pairs']:2d} | {r['interpretation']}")
