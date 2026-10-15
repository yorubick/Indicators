import json
from collections import Counter

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = d.get("cases", [])

# Group by (symbol, session, START, dt) and sort by bars
series = {}
for c in cases:
    if c.get("C_Lite") is not None and c.get("bars", 0) >= 21:
        key = (c.get("START"), c.get("dt"))
        series.setdefault(key, []).append(c)

print(f"Total series with >= 2 long cases: {sum(1 for s in series.values() if len(s) >= 2)}")

step_diffs = []
for key, s in series.items():
    s_sorted = sorted(s, key=lambda x: x["bars"])
    for i in range(len(s_sorted) - 1):
        c1 = s_sorted[i]
        c2 = s_sorted[i+1]
        delta_bars = c2["bars"] - c1["bars"]
        delta_c = round(c2["C_Lite"] - c1["C_Lite"], 4)
        step_diffs.append({
            "start": key[0],
            "dt": key[1],
            "b1": c1["bars"],
            "b2": c2["bars"],
            "delta_bars": delta_bars,
            "c1": round(c1["C_Lite"], 2),
            "c2": round(c2["C_Lite"], 2),
            "delta_c": delta_c
        })

print(f"Total adjacent transitions: {len(step_diffs)}")
one_bar_steps = [s for s in step_diffs if s["delta_bars"] == 1]
print(f"One-bar steps: {len(one_bar_steps)}")

counts = Counter(s["delta_c"] for s in one_bar_steps)
print("Distribution of Delta C for 1-bar addition:")
for delta, count in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  Delta C = {delta:+7.2f} : {count:3d} times")

print("\nSample one-bar steps:")
for s in one_bar_steps[:15]:
    print(f"dt={s['dt']:2d}s | bars {s['b1']:2d}->{s['b2']:2d} | C: {s['c1']:5.1f} -> {s['c2']:5.1f} | Delta C: {s['delta_c']:+5.1f}")
