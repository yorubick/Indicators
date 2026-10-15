import json
from pathlib import Path

p = Path("G:/trading/guias/analisis/C_matriz.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

for i in [10, 11, 12, 13, 14, 15, 16, 17, 18]:
    c = d["cases"][i]
    print(f"[{i:2d}] {c['START']} - {c['END']} n={c['bars']}: C = {c['C']:.12f}")
