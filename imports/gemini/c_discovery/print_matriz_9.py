import json

with open(r"G:\trading\guias\analisis\C_matriz_frontera15s.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for c in data["cases"]:
    start = c["START"].split("T")[1][:8]
    end = c["END"].split("T")[1][:8]
    bars = c["bars"]
    c_val = c["C"]
    print(f"START: {start} | END: {end} | bars: {bars:2d} | C: {c_val:6.2f}")
