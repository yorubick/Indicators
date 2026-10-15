import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

long_cases = [c for c in data['cases'] if c['bars'] >= 21]

rows = []
for c in long_cases:
    ohlc = c['OHLC']
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    opens = [x['open'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    
    rng = max(highs) - min(lows)
    start_pos = (opens[0] - min(lows)) / rng if rng > 0 else 0.5
    end_pos = (closes[-1] - min(lows)) / rng if rng > 0 else 0.5
    first_rng = highs[0] - lows[0]
    first_body = abs(closes[0] - opens[0])
    
    rows.append({
        'id': c['id'][:25],
        'split': c['split'],
        'START': c['START'][11:16],
        'END': c['END'][11:16],
        'n': c['bars'],
        'dt': c['dt'],
        'C': round(c['C']),
        'start_pos': round(start_pos, 3),
        'end_pos': round(end_pos, 3),
        'first_rng': round(first_rng, 2),
        'rng': round(rng, 2)
    })

df = pd.DataFrame(rows)
print(df[df['START'].str.startswith('19:')].to_string())
