import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

with open(r'G:\trading\guias\analisis\C_evolucion87_resultados.json') as f:
    data13 = json.load(f)

with open(r'G:\trading\guias\analisis\C_evolucion87_predicciones.json') as f:
    pred13 = json.load(f)

full_ohlc_13 = pred13['OHLC']

# Collect all long cases with dt=60
long_cases = []
for c in data['cases']:
    if c['bars'] >= 21 and c['dt'] == 60:
        ohlc = c['OHLC']
        highs = [x['high'] for x in ohlc]
        lows = [x['low'] for x in ohlc]
        opens = [x['open'] for x in ohlc]
        closes = [x['close'] for x in ohlc]
        rng = max(highs) - min(lows)
        trs = [highs[0]-lows[0]] + [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, len(closes))]
        atr = np.mean(trs)
        
        long_cases.append({
            'id': c['id'],
            'split': c['split'],
            'bars': c['bars'],
            'C': round(c['C']),
            'rng': rng,
            'atr': round(atr, 2),
            'rng_atr': round(rng / atr, 2),
            'open0': opens[0],
            'close_end': closes[-1],
            'dir': 'BULL' if closes[-1] > opens[0] else 'BEAR',
            'start_pos': round((opens[0] - min(lows)) / rng, 2) if rng > 0 else 0.5,
            'end_pos': round((closes[-1] - min(lows)) / rng, 2) if rng > 0 else 0.5
        })

# Add Oct 13 cases
for c in data13['cases']:
    sub = full_ohlc_13[:c['bars']]
    highs = [x['high'] for x in sub]
    lows = [x['low'] for x in sub]
    opens = [x['open'] for x in sub]
    closes = [x['close'] for x in sub]
    rng = max(highs) - min(lows)
    trs = [highs[0]-lows[0]] + [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, len(closes))]
    atr = np.mean(trs)
    long_cases.append({
        'id': f"oct13_{c['END'][11:16]}",
        'split': 'oct13_fresh',
        'bars': c['bars'],
        'C': round(c['C']),
        'rng': rng,
        'atr': round(atr, 2),
        'rng_atr': round(rng / atr, 2),
        'open0': opens[0],
        'close_end': closes[-1],
        'dir': 'BULL' if closes[-1] > opens[0] else 'BEAR',
        'start_pos': round((opens[0] - min(lows)) / rng, 2) if rng > 0 else 0.5,
        'end_pos': round((closes[-1] - min(lows)) / rng, 2) if rng > 0 else 0.5
    })

df = pd.DataFrame(long_cases)
print("Total long cases (dt=60):", len(df))
print(df.to_string())
