import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

long_cases = [c for c in data['cases'] if c['bars'] >= 21]

rows = []
for c in long_cases:
    n = c['bars']
    dt = c['dt']
    C = round(c['C'])
    t_span = (n - 1) * dt
    m = t_span / C
    m_round = round(m)
    err = abs(m - m_round)
    
    # Check if floor(t_span / m_round) == C or round(t_span / m_round) == C
    pred_floor = int(np.floor(t_span / m_round)) if m_round > 0 else 0
    pred_round = int(np.round(t_span / m_round)) if m_round > 0 else 0
    
    rows.append({
        'id': c['id'][:25],
        'split': c['split'],
        'START': c['START'][11:16],
        'END': c['END'][11:16],
        'n': n,
        'dt': dt,
        'C': C,
        't_span': t_span,
        'M_exact': round(m, 3),
        'M_int': m_round,
        'M_err': round(err, 3),
        'match_floor': (pred_floor == C),
        'match_round': (pred_round == C)
    })

df = pd.DataFrame(rows)
print(f"Total long cases: {len(df)}")
print(f"Exact match with floor(TimeSpan / M_int): {df['match_floor'].sum()} / {len(df)} ({df['match_floor'].mean()*100:.1f}%)")
print(f"Exact match with round(TimeSpan / M_int): {df['match_round'].sum()} / {len(df)} ({df['match_round'].mean()*100:.1f}%)")

print("\nDistribution of M_int across all cases:")
print(df['M_int'].value_counts().sort_index())
