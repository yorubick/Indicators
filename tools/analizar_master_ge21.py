import json
import pandas as pd
import numpy as np

data = json.load(open('master_all_C_cases.json'))
cases = data['cases']
ge21 = [c for c in cases if c['bars'] >= 21]

print(f"Total cases: {len(cases)}, bars >= 21: {len(ge21)}")
rows = []
for c in ge21:
    n = c['bars']
    dt = c['dt']
    t_elap = (n - 1) * dt
    t_inc = n * dt
    c_val = c['C']
    kappa = t_elap / c_val if c_val > 0 else 0
    rows.append({
        'id': c['id'],
        'bars': n,
        'dt': dt,
        'T_elap': t_elap,
        'C': round(c_val, 4),
        'kappa': round(kappa, 2)
    })

df = pd.DataFrame(rows)
print(df.head(20).to_string())
print("\nDistribución de kappa (cuantiles y valores comunes):")
print(df['kappa'].describe())
print("\nValores más frecuentes de kappa redondeado a 0.5:")
print((df['kappa'] * 2).round() / 2)
