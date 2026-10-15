import json
from pathlib import Path

records = []

def add_case(src, start, end, n, c, high, low, tf=60):
    try:
        c = float(c)
        n = int(n)
        high = float(high)
        low = float(low)
        # normalize start / end
        if "T" in str(start):
            start = str(start).split("T")[1][:5]
        else:
            start = str(start)[:5]
        if "T" in str(end):
            end = str(end).split("T")[1][:5]
        else:
            end = str(end)[:5]
        records.append({
            "source": src,
            "start": start,
            "end": end,
            "n": n,
            "C": round(c, 4),
            "high": high,
            "low": low,
            "range": round(high - low, 2),
            "tf": tf
        })
    except Exception as e:
        pass

# Scan all json files in G:/trading/guias/analisis
p = Path("G:/trading/guias/analisis")
for fpath in p.glob("*.json"):
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        cases = []
        if isinstance(data, dict):
            if "cases" in data:
                cases = data["cases"]
            elif "records" in data:
                cases = data["records"]
        elif isinstance(data, list):
            cases = data
        for c in cases:
            if isinstance(c, dict) and "C" in c:
                st = c.get("START", c.get("start", ""))
                en = c.get("END", c.get("end", ""))
                n = c.get("bars", c.get("n", 0))
                c_val = c.get("C")
                h = c.get("high", c.get("high_global", 0))
                l = c.get("low", c.get("low_global", 0))
                tf = c.get("chart_seconds", c.get("source_seconds", 60))
                if st and en and c_val is not None:
                    add_case(fpath.name, st, en, n, c_val, h, l, tf)
    except Exception as e:
        pass

print(f"Total collected: {len(records)}")

seen = set()
unique = []
for r in records:
    key = (r["tf"], r["start"], r["end"], r["n"], round(r["C"], 2))
    if key not in seen:
        seen.add(key)
        unique.append(r)

print(f"Total unique: {len(unique)}")
unique.sort(key=lambda x: (x["tf"], x["n"], x["start"], x["end"]))

print(f"\n{'TF':4s} {'START':6s} {'END':6s} {'n':3s} {'C':8s} {'Range':8s} {'High':10s} {'Low':10s} {'Source':25s}")
for r in unique:
    print(f"{r['tf']:4d} {r['start']:6s} {r['end']:6s} {r['n']:3d} {r['C']:8.2f} {r['range']:8.2f} {r['high']:10.2f} {r['low']:10.2f} {r['source']:25s}")
