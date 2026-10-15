import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = {c["id"]: c for c in d["cases"]}

ids_77 = [
    "20261012_185800_191800_60s",
    "20261012_185900_191900_60s",
    "20261012_190000_192000_60s",
    "20261012_190100_192100_60s"
]

for cid in ids_77:
    c = cases[cid]
    ohlc = c["OHLC"]
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    wh = max(highs)
    wl = min(lows)
    ih = highs.index(wh)
    il = lows.index(wl)
    n = len(ohlc)
    print(f"{cid[:25]} | C={c['C_Lite']:.1f} | High={wh} at bar {ih} ({ohlc[ih]['time']}) | Low={wl} at bar {il} ({ohlc[il]['time']}) | DistToEndH={n-1-ih} DistToEndL={n-1-il}")
