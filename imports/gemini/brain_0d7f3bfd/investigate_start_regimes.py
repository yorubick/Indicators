import json
from pathlib import Path

path = Path("G:/trading/guias/analisis/C_START_regimenes.json")
with open(path, "r", encoding="utf-8") as f:
    d = json.load(f)

print("=== C_START_REGIMENES CASES ===")
for c in d["cases"]:
    start = c["START"][11:16]
    end = c["END"][11:16]
    print(f"[{start} - {end}] n={c['bars']:2d} C={c['C']:10.4f} H={c['high']} L={c['low']} regime={c['regime']}")
