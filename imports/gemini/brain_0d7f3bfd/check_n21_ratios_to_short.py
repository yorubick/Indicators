import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

cases_21 = [c for c in data['cases'] if c['bars'] == 21 and c['dt'] == 60]

print(f"{'Case':26s} | Actual C | Short Pred (68.85) | Ratio C / Pred | Range | ATR   | Net")
print("-" * 80)
for c in sorted(cases_21, key=lambda x: round(x['C'])):
    C = round(c['C'])
    pred = 21 * 60 * 10 / 183 # 68.852
    ratio = C / pred
    
    ohlc = c['OHLC']
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    rng = max(highs) - min(lows)
    trs = [highs[0]-lows[0]] + [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, len(closes))]
    atr = np.mean(trs)
    net = closes[-1] - ohlc[0]['open']
    
    label = f"{c['split'][:5]} {c['START'][11:16]}->{c['END'][11:16]}"
    print(f"{label:26s} | {C:8d} | {pred:18.2f} | {ratio:14.3f} | {rng:5.2f} | {atr:5.2f} | {net:6.2f}")
