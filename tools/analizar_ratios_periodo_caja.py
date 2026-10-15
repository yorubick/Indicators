import json
import pandas as pd
import numpy as np

master = json.load(open("master_all_C_cases.json", encoding="utf-8"))
cases = [c for c in master["cases"] if c["bars"] >= 21 and c.get("C_Lite") is not None]

rows = []
for c in cases:
    n = c["bars"]
    dt = c["dt"]
    c_val = c["C_Lite"]
    
    # Período efectivo de Lane 3 A en barras
    N_3a = (24.0 * c_val) / dt
    
    # Relación con la longitud de la caja (n - 1)
    span = n - 1
    ratio_N_span = N_3a / span if span > 0 else 0
    
    rows.append({
        'id': c['id'],
        'dt': dt,
        'n': n,
        'C': c_val,
        'N_3a': N_3a,
        'span': span,
        'ratio': ratio_N_span
    })

df = pd.DataFrame(rows)

print("=== DISTRIBUCIÓN DEL RATIO N_3a / (n - 1) ===")
print("Estadísticas del ratio período_EMA / longitud_caja:")
print(df['ratio'].describe())

print("\nValores más frecuentes del ratio N_3a / span (redondeado a 2 decimales):")
print(df['ratio'].round(2).value_counts().head(15))
