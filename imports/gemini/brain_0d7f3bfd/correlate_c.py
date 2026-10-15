import json
import numpy as np

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

long_cases = [c for c in data['cases'] if c['bars'] >= 21 and c['dt'] == 60]

print(f"Total long 60s cases: {len(long_cases)}")

# Let's extract candidate terms:
# n, range, atr, ticks, time_span, net, path, er, start_pos, end_pos
X = []
Y = []
case_info = []

for c in long_cases:
    ohlc = c['OHLC']
    n = c['bars']
    C = round(c['C'])
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    opens = [x['open'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    
    rng = max(highs) - min(lows)
    trs = [highs[0]-lows[0]] + [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, len(closes))]
    atr = np.mean(trs)
    net = abs(closes[-1] - opens[0])
    path = sum(abs(closes[i] - closes[i-1]) for i in range(1, len(closes)))
    er = net / path if path > 0 else 0
    ticks = rng / 0.25
    
    start_pos = (opens[0] - min(lows)) / rng if rng > 0 else 0.5
    end_pos = (closes[-1] - min(lows)) / rng if rng > 0 else 0.5
    
    X.append({
        'n': n,
        'rng': rng,
        'atr': atr,
        'ticks': ticks,
        'net': net,
        'path': path,
        'er': er,
        'start_pos': start_pos,
        'end_pos': end_pos,
        't_span': (n - 1) * 60,
        'c_short': n * 60 * 10 / 183
    })
    Y.append(C)
    case_info.append(f"{c['START'][11:16]}->{c['END'][11:16]} (C={C})")

import pandas as pd
df_X = pd.DataFrame(X)
df_X['C'] = Y

print("\nCorrelations with C:")
corrs = df_X.corr()['C'].sort_values(ascending=False)
print(corrs)
