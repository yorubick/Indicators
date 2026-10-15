import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = d.get("cases", [])
long_cases = [c for c in cases if c.get("bars", 0) >= 21 and c.get("C_Lite") is not None]
print(f"Total long Lite cases: {len(long_cases)}")

# Analyze invariants on long cases:
# Features that are scale invariant (P -> 2P), translation invariant (P -> P + 10000), reflection invariant (P -> -P)
for c in long_cases[:10]:
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    c_val = c["C_Lite"]
    
    # 1. Bar of highest high (0-indexed from start)
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    max_h = max(highs)
    min_l = min(lows)
    
    # indices
    idx_high = highs.index(max_h)
    idx_low = lows.index(min_l)
    
    # Distances in bars and seconds
    dist_high_low_bars = abs(idx_high - idx_low)
    dist_high_low_sec = dist_high_low_bars * dt
    
    dist_start_first_extreme = min(idx_high, idx_low) * dt
    dist_last_extreme_end = (n - 1 - max(idx_high, idx_low)) * dt
    
    # Base theoretical
    T = (n - 1) * dt
    T_inc = n * dt
    base_183 = T_inc / 18.3
    
    print(f"ID: {c['id'][:25]} | n={n} dt={dt} | C={c_val:.1f} | Base={base_183:.1f} | Diff={c_val - base_183:+.1f} | HighBar={idx_high} LowBar={idx_low} | DistHL={dist_high_low_sec}s")
