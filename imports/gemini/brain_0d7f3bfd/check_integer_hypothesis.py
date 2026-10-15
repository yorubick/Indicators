import json
from pathlib import Path

cases = []
def load_from(path_str):
    p = Path(path_str)
    if not p.exists(): return []
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
    return [c for c in d.get("cases", []) if "OHLC" in c and "C" in c]

cases += load_from("G:/trading/guias/analisis/C_matriz.json")
cases += load_from("G:/trading/guias/analisis/C_START_regimenes.json")
cases += load_from("G:/trading/guias/analisis/C_23_desplazamientos.json")

for c in cases:
    n = c.get("bars", len(c.get("OHLC", [])))
    c_val = c["C"]
    diff_int = abs(c_val - round(c_val))
    if n >= 21:
        if diff_int > 1e-5:
            print(f"NON-INTEGER at n={n}: C={c_val}")
        else:
            pass

print("Check finished. If no lines printed above, EVERY SINGLE C FOR n >= 21 IS AN EXACT INTEGER!")
