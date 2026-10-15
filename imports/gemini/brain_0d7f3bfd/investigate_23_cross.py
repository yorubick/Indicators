import json
from pathlib import Path

path_23 = Path("G:/trading/guias/analisis/C_23_desplazamientos.json")
with open(path_23, "r", encoding="utf-8") as f:
    d23 = json.load(f)

print("=== C_23_DESPLAZAMIENTOS CASES ===")
for c in d23["cases"]:
    start = c["START"][11:16]
    end = c["END"][11:16]
    print(f"[{start} - {end}] n={c['bars']} C={c['C']} H={c['high']} L={c['low']} cross={c['cross_control']}")

print("\n=== CHANGES BETWEEN CONSECUTIVE CASES ===")
for ch in d23["changes"]:
    print(f"{ch['from'][11:16]} -> {ch['to'][11:16]}: C {ch['C_from']} -> {ch['C_to']}")
    if ch["removed"]:
        rem = ch["removed"][0]
        print(f"  Removed: {rem['time']} O={rem['open']} H={rem['high']} L={rem['low']} C={rem['close']}")
    if ch["added"]:
        add = ch["added"][0]
        print(f"  Added:   {add['time']} O={add['open']} H={add['high']} L={add['low']} C={add['close']}")
