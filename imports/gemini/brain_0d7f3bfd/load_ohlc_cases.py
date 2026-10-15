import json
from pathlib import Path

# Load all detailed cases where we have OHLC data:
# 1. C_matriz.json (24 cases)
# 2. C_START_regimenes.json (12 cases)
# 3. C_23_desplazamientos.json (7 cases)

cases = []

def load_from(path_str):
    p = Path(path_str)
    if not p.exists(): return []
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
    cs = d.get("cases", [])
    res = []
    for c in cs:
        if "OHLC" in c and "C" in c:
            res.append(c)
    return res

cases += load_from("G:/trading/guias/analisis/C_matriz.json")
cases += load_from("G:/trading/guias/analisis/C_START_regimenes.json")
cases += load_from("G:/trading/guias/analisis/C_23_desplazamientos.json")

print(f"Loaded {len(cases)} cases with full OHLC.")

# Filter to cases with n >= 21
cases_21 = [c for c in cases if c.get("bars", len(c.get("OHLC", []))) >= 21]
print(f"Cases with n >= 21: {len(cases_21)}")

for i, c in enumerate(cases_21):
    st = c.get("START", "")[11:16] if "T" in c.get("START", "") else c.get("START", "")[:5]
    en = c.get("END", "")[11:16] if "T" in c.get("END", "") else c.get("END", "")[:5]
    n = c.get("bars", len(c["OHLC"]))
    c_val = c["C"]
    print(f"[{i:2d}] {st} - {en} n={n:2d} C={c_val:6.2f}")
