import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

with open(r'G:\trading\guias\analisis\C_evolucion87_resultados.json') as f:
    data13 = json.load(f)

# Collect training cases
train_cases = [c for c in data['cases'] if c['branch'] == 'long' and c['split'] == 'training']
# Add 13 Oct calibration cases
for c in data13['cases'][:2]: # first 2 were calibration (06:45, 06:46)
    train_cases.append({
        'id': f"oct13_{c['END'][11:16]}",
        'START': '2026-10-13T06:25:00+00:00',
        'END': c['END'],
        'bars': c['bars'],
        'dt': 60,
        'C': c['C'],
        'split': 'training',
        'OHLC': None,
        'range_high': c['range_high'],
        'range_low': c['range_low']
    })

print(f"Total training cases: {len(train_cases)}")

# Test candidate formulas for Sub-branch 2C on the training cases
# We want to predict C for all cases that are NOT consolidation or breakout
macro_train = []
for c in train_cases:
    if c['id'] in ['20261012_190000_190500_15s']:
        continue # 15s
    if c.get('OHLC') is None:
        rng = c['range_high'] - c['range_low']
        macro_train.append({'id': c['id'], 'C': round(c['C']), 'rng': rng, 'n': c['bars'], 'dt': c['dt']})
        continue
        
    ohlc = c['OHLC']
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    opens = [x['open'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    
    rng = max(highs) - min(lows)
    start_pos = (opens[0] - min(lows)) / rng if rng > 0 else 0.5
    is_new_high = highs[-1] > max(highs[:-1])
    n = c['bars']
    dt = c['dt']
    t_span = (n - 1) * dt
    C = round(c['C'])
    
    # Exclude consolidation and breakout
    is_consol = (rng <= 22.25 and start_pos >= 0.40 and not is_new_high and n <= 25)
    is_breakout = (is_new_high and rng <= 26.0 and start_pos >= 0.35)
    
    if not is_consol and not is_breakout:
        trs = [highs[0]-lows[0]] + [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, len(closes))]
        atr = np.mean(trs)
        macro_train.append({
            'id': c['id'],
            'C': C,
            'rng': rng,
            'atr': atr,
            'n': n,
            'dt': dt,
            'start_pos': start_pos
        })

df_macro = pd.DataFrame(macro_train)
print(f"Macro training cases: {len(df_macro)}")
print(df_macro[['id', 'C', 'rng', 'n']].to_string())

# Test various parameterizations on df_macro:
# Model A: Discrete rungs based on Range thresholds:
# If Range > 80 -> C = 68 (or 62)
# If 40 < Range <= 80 -> C = 77
# If 25 < Range <= 40 -> C = 84 (or 81)
# If Range <= 25 and start_pos < 0.25 -> C = 77
