import json
import pandas as pd
import numpy as np

master = json.load(open("master_all_C_cases.json", encoding="utf-8"))
cases = [c for c in master["cases"] if c["bars"] >= 21 and c.get("C_Lite") is not None]

print(f"Total long cases with C_Lite: {len(cases)}")

# Let's inspect ratios of T / C and find clusters of exact divisors
divisors = []
for c in cases:
    n = c["bars"]
    dt = c["dt"]
    T_inclusive = n * dt
    T_exclusive = (n - 1) * dt
    c_val = c["C_Lite"]
    
    div_inc = T_inclusive / c_val
    div_exc = T_exclusive / c_val
    
    divisors.append({
        'id': c['id'],
        'dt': dt,
        'n': n,
        'C': c_val,
        'div_inc': div_inc,
        'div_exc': div_exc,
        'round_c': round(c_val)
    })

df = pd.DataFrame(divisors)

print("\n--- DISTRIBUCIÓN DE DIVISORES T / C ---")
print("Top 10 valores más comunes de C y sus divisores promedio T_exclusive / C:")
top_c = df['round_c'].value_counts().head(10)
for c_target in top_c.index:
    sub = df[df['round_c'] == c_target]
    print(f"C = {c_target:3d} (N={len(sub):2d}): mean T_exc/C = {sub['div_exc'].mean():.2f}, min={sub['div_exc'].min():.2f}, max={sub['div_exc'].max():.2f}, mean n={sub['n'].mean():.1f}")
