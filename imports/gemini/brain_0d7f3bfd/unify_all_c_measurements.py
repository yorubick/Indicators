import json
from pathlib import Path

records = []

# 1. C_START_regimenes.json
p1 = Path("G:/trading/guias/analisis/C_START_regimenes.json")
if p1.exists():
    with open(p1, "r", encoding="utf-8") as f:
        d = json.load(f)
    for c in d.get("cases", []):
        records.append({
            "source_file": "C_START_regimenes.json",
            "start": c["START"][11:16],
            "end": c["END"][11:16],
            "n": c["bars"],
            "C": round(c["C"], 4),
            "high": c["high"],
            "low": c["low"],
            "range": round(c["high"] - c["low"], 2),
            "timeframe": 60,
            "regime": c.get("regime", "")
        })

# 2. C_23_desplazamientos.json
p2 = Path("G:/trading/guias/analisis/C_23_desplazamientos.json")
if p2.exists():
    with open(p2, "r", encoding="utf-8") as f:
        d = json.load(f)
    for c in d.get("cases", []):
        records.append({
            "source_file": "C_23_desplazamientos.json",
            "start": c["START"][11:16],
            "end": c["END"][11:16],
            "n": c["bars"],
            "C": round(c["C"], 4),
            "high": c["high"],
            "low": c["low"],
            "range": round(c["high"] - c["low"], 2),
            "timeframe": 60,
            "regime": "shift23"
        })

# 3. C_21_regimenes.json
p3 = Path("G:/trading/guias/analisis/C_21_regimenes.json")
if p3.exists():
    with open(p3, "r", encoding="utf-8") as f:
        d = json.load(f)
    for c in d.get("cases", []):
        records.append({
            "source_file": "C_21_regimenes.json",
            "start": c["START"][11:16],
            "end": c["END"][11:16],
            "n": c["bars"],
            "C": round(c["C"], 4),
            "high": c["high"],
            "low": c["low"],
            "range": round(c["high"] - c["low"], 2),
            "timeframe": 60,
            "regime": c.get("regime", "")
        })

# 4. C_matriz.json
p4 = Path("G:/trading/guias/analisis/C_matriz.json")
if p4.exists():
    with open(p4, "r", encoding="utf-8") as f:
        d = json.load(f)
    cases = d if isinstance(d, list) else d.get("cases", [])
    for c in cases:
        st = c.get("START", "")
        en = c.get("END", "")
        if len(st) >= 16 and len(en) >= 16:
            records.append({
                "source_file": "C_matriz.json",
                "start": st[11:16],
                "end": en[11:16],
                "n": c.get("bars", 0),
                "C": round(c.get("C", 0), 4),
                "high": c.get("high", 0),
                "low": c.get("low", 0),
                "range": round(c.get("high", 0) - c.get("low", 0), 2),
                "timeframe": c.get("chart_seconds", 60),
                "regime": "matriz"
            })

print(f"Total collected records: {len(records)}")
# Deduplicate by (start, end, timeframe)
seen = set()
unique_records = []
for r in records:
    key = (r["start"], r["end"], r["timeframe"], r["n"])
    if key not in seen:
        seen.add(key)
        unique_records.append(r)

print(f"Total unique records: {len(unique_records)}")

# Sort by timeframe, n, start, end
unique_records.sort(key=lambda x: (x["timeframe"], x["n"], x["start"], x["end"]))

print(f"\n{'TF':4s} {'START':6s} {'END':6s} {'n':3s} {'C':8s} {'Range':8s} {'High':10s} {'Low':10s} {'File':25s}")
for r in unique_records:
    print(f"{r['timeframe']:4d} {r['start']:6s} {r['end']:6s} {r['n']:3d} {r['C']:8.2f} {r['range']:8.2f} {r['high']:10.2f} {r['low']:10.2f} {r['source_file']:25s}")
