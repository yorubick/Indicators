import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

cases = master["cases"]
c77_cases = [c for c in cases if abs((c.get("C_Lite") or c.get("C") or 0) - 77.0) < 1.0 and ("19:" in c.get("START", "") or "18:" in c.get("START", ""))]

for c in c77_cases:
    bars = c["OHLCV"]
    h = max(b["high"] for b in bars)
    l = min(b["low"] for b in bars)
    rng = h - l
    h_idx = [i for i, b in enumerate(bars) if b["high"] == h]
    l_idx = [i for i, b in enumerate(bars) if b["low"] == l]
    s = c["START"][11:16]
    e = c["END"][11:16]
    n = c["bars"]
    print(f"{s} -> {e} (n={n}) | H={h} (idx {h_idx}) | L={l} (idx {l_idx}) | Range={rng}")
