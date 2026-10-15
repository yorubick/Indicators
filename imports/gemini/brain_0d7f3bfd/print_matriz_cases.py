import json, datetime
from pathlib import Path

p = Path("G:/trading/guias/analisis/C_matriz.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

print("Cases in C_matriz:")
for i, c in enumerate(d["cases"]):
    print(f"[{i:2d}] {c['START']} - {c['END']} (n={c['bars']}): C={c['C']:.2f} H={c['high']} L={c['low']}")
