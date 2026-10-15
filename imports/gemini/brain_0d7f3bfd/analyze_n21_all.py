import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

cases_21 = [c for c in data['cases'] if c['bars'] == 21 and c['dt'] == 60]

print(f"Total n=21, dt=60 cases: {len(cases_21)}")

rows = []
for c in cases_21:
    ohlc = c['OHLC']
    highs = np.array([x['high'] for x in ohlc])
    lows = np.array([x['low'] for x in ohlc])
    closes = np.array([x['close'] for x in ohlc])
    opens = np.array([x['open'] for x in ohlc])
    
    C = round(c['C'])
    rng = np.max(highs) - np.min(lows)
    ticks = rng / 0.25
    
    # ATR
    trs = [highs[0] - lows[0]]
    for i in range(1, len(highs)):
        trs.append(max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1])))
    atr = np.mean(trs)
    
    imax = int(np.argmax(highs))
    imin = int(np.argmin(lows))
    dist_hl = abs(imax - imin)
    
    # Position of end bar relative to range
    end_pos = (closes[-1] - np.min(lows)) / rng if rng > 0 else 0.5
    start_pos = (opens[0] - np.min(lows)) / rng if rng > 0 else 0.5
    
    # Volume sum if present
    vol = sum(x.get('volume', 0) for x in ohlc)
    
    rows.append({
        'id': c['id'][:25],
        'split': c['split'],
        'START': c['START'][11:16],
        'END': c['END'][11:16],
        'C': C,
        'range': rng,
        'ticks': ticks,
        'atr': round(atr, 2),
        'dist_hl': dist_hl,
        'imax': imax,
        'imin': imin,
        'start_pos': round(start_pos, 2),
        'end_pos': round(end_pos, 2),
        'net': round(closes[-1] - opens[0], 2)
    })

df = pd.DataFrame(rows).sort_values('C')
print(df.to_string())
