import json
from collections import defaultdict
import numpy as np

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = [c for c in d["cases"] if c.get("bars", 0) >= 21 and c.get("C_Lite") is not None]

# Test hypothesis: Does END bar making a new global extreme correlate with large C or positive jumps?
end_extreme_cases = []
internal_end_cases = []

for c in cases:
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    c_val = c["C_Lite"]
    base_183 = round((n * dt) / 18.3)
    res = c_val - base_183
    
    highs = [b["high"] for b in ohlc]
    lows = [b["low"] for b in ohlc]
    
    max_h = max(highs)
    min_l = min(lows)
    
    end_h = highs[-1]
    end_l = lows[-1]
    
    is_new_high = (end_h == max_h)
    is_new_low = (end_l == min_l)
    is_extreme = is_new_high or is_new_low
    
    entry = {
        "id": c["id"],
        "dt": dt,
        "n": n,
        "C": c_val,
        "base": base_183,
        "res": res,
        "is_new_high": is_new_high,
        "is_new_low": is_new_low,
        "is_extreme": is_extreme
    }
    
    if is_extreme:
        end_extreme_cases.append(entry)
    else:
        internal_end_cases.append(entry)

print(f"Total long cases: {len(cases)}")
print(f"Cases where END is a new extreme (High or Low): {len(end_extreme_cases)} ({len(end_extreme_cases)/len(cases)*100:.1f}%)")
print(f"Cases where END is internal: {len(internal_end_cases)} ({len(internal_end_cases)/len(cases)*100:.1f}%)")

res_ext = [e["res"] for e in end_extreme_cases]
res_int = [e["res"] for e in internal_end_cases]

print(f"\nResiduals when END is a NEW EXTREME:")
print(f"  Mean: {np.mean(res_ext):+.2f} | Median: {np.median(res_ext):+.2f} | Min: {min(res_ext):+.2f} | Max: {max(res_ext):+.2f}")

print(f"\nResiduals when END is INTERNAL:")
print(f"  Mean: {np.mean(res_int):+.2f} | Median: {np.median(res_int):+.2f} | Min: {min(res_int):+.2f} | Max: {max(res_int):+.2f}")

# Look at 1-bar steps where END transitioned from internal to extreme or vice versa
from analyze_delta_c_steps import one_bar_steps

print("\n1-Bar Steps analysis by extreme status:")
ext_transitions = []
for s in one_bar_steps:
    # Find matching case c2
    # Check if delta C is positive when c2 is an extreme
    pass
