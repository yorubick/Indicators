import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

with open(r'G:\trading\guias\analisis\C_evolucion87_resultados.json') as f:
    data13 = json.load(f)

# Combine long cases
long_cases = [c for c in data['cases'] if c['bars'] >= 21]

# Add Oct 13 cases
for c in data13['cases']:
    long_cases.append({
        'id': f"20261013_{c['END'][11:16]}_60s",
        'START': '2026-10-13T06:25:00+00:00',
        'END': c['END'],
        'bars': c['bars'],
        'dt': 60,
        'C': c['C'],
        'split': 'validation_oct13',
        'OHLC': None,
        'range_high': c['range_high'],
        'range_low': c['range_low']
    })

print(f"Total long cases to audit: {len(long_cases)}")

rows = []
for c in long_cases:
    dt = c['dt']
    C = round(c['C'])
    n = c['bars']
    t_span = (n - 1) * dt
    
    # Lambda = C / dt
    lam = C / dt
    
    # Nearest step on the 0.05 grid (step = 0.05 * dt)
    step_sec = 0.05 * dt
    k_float = (C - 63.0 * (dt / 60.0)) / step_sec
    k_round = round(k_float)
    
    # Ladder prediction:
    c_ladder = round(63.0 * (dt / 60.0) + k_round * step_sec)
    res = C - c_ladder
    
    # Also check if it belongs to consolidation branch floor(t_span / 24)
    c_consol = int(np.floor(t_span / 24.0))
    res_consol = C - c_consol
    
    # Best branch
    is_consol = (abs(res_consol) == 0 and n <= 25 and C <= 60)
    
    rows.append({
        'id': c['id'][:25],
        'split': c['split'],
        'n': n,
        'dt': dt,
        'C': C,
        'lambda': round(lam, 3),
        'k_ladder': k_round,
        'C_ladder': c_ladder,
        'res_ladder': res,
        'is_consol': is_consol,
        'C_consol': c_consol,
    })

df = pd.DataFrame(rows)

print("\n=== LADDER AUDIT SUMMARY ===")
print("Distribution of residuals to nearest ladder rung (step = 3s for 60s):")
print(df['res_ladder'].value_counts().sort_index())

print("\nBreakdown by residual:")
exact_ladder = (df['res_ladder'] == 0).sum()
within_1s = (df['res_ladder'].abs() <= 1).sum()
print(f"Exact match on ladder (res = 0): {exact_ladder} / {len(df)} ({exact_ladder/len(df)*100:.1f}%)")
print(f"Within +/- 1s of ladder:         {within_1s} / {len(df)} ({within_1s/len(df)*100:.1f}%)")

print("\nCases with residual == 0 (Exact ladder rungs):")
print(df[df['res_ladder'] == 0][['id', 'split', 'n', 'dt', 'C', 'lambda', 'k_ladder']].to_string())

print("\nCases with residual != 0:")
print(df[df['res_ladder'] != 0][['id', 'split', 'n', 'dt', 'C', 'lambda', 'k_ladder', 'res_ladder', 'is_consol']].to_string())
