import json
from pathlib import Path

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

print(f"{'ID':30s} {'split':10s} {'n':3s} {'dt':3s} {'C':5s} {'24*C/dt':9s} {'72*C/dt':9s}")
for c in d["cases"]:
    if c["branch"] == "long":
        dt = c["dt"]
        c_val = c["C"]
        n = c["bars"]
        p24 = 24.0 * c_val / dt
        p72 = 72.0 * c_val / dt
        print(f"{c['id']:30s} {c['split']:10s} {n:3d} {dt:3d} {round(c_val):4d} {p24:9.3f} {p72:9.3f}")
