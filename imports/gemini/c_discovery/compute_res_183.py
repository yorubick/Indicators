import json
from collections import Counter
import numpy as np

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = [c for c in d["cases"] if c.get("bars", 0) >= 21 and c.get("C_Lite") is not None]

print(f"Total long cases: {len(cases)}")

residuals = []
for c in cases:
    n = c["bars"]
    dt = c["dt"]
    T = n * dt # inclusive duration
    c_obs = c["C_Lite"]
    
    # Test divisors around 18.3: 18.3, 18.0, 183/10
    base_183 = round(T / 18.3)
    res_183 = round(c_obs - base_183, 2)
    
    residuals.append({
        "id": c["id"],
        "dt": dt,
        "n": n,
        "T": T,
        "C_obs": round(c_obs, 2),
        "base_183": base_183,
        "res_183": res_183
    })

res_vals = [r["res_183"] for r in residuals]
counts = Counter(res_vals)

print(f"Residual Statistics (C_obs - round(T / 18.3)):")
print(f"Mean: {np.mean(res_vals):.2f}")
print(f"Median: {np.median(res_vals):.2f}")
print(f"Std: {np.std(res_vals):.2f}")
print(f"MAE: {np.mean(np.abs(res_vals)):.2f}")
print(f"Min: {min(res_vals):.2f}, Max: {max(res_vals):.2f}")

print("\nTop most frequent residuals:")
for val, count in counts.most_common(15):
    print(f"  Residual {val:+6.1f} s : {count:3d} cases ({count/len(cases)*100:.1f}%)")
