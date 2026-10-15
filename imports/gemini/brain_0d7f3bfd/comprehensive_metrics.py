import json
import numpy as np

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

cases = data['cases']
long_cases = [c for c in cases if c['bars'] >= 21]

print("Case ID | n | dt | C | High - Low | ATR | Net | C / dt | (n*dt)/C | C / n")
print("-" * 80)
for c in sorted(long_cases, key=lambda x: (x['split'], x['START'], x['bars'])):
    n = c['bars']
    dt = c['dt']
    C = round(c['C'])
    ohlc = c['OHLC']
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    rng = max(highs) - min(lows)
    net = closes[-1] - ohlc[0]['open']
    
    # ATR
    trs = [highs[0] - lows[0]]
    for i in range(1, len(highs)):
        trs.append(max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1])))
    atr = np.mean(trs)
    
    t_span = (n - 1) * dt
    ratio_m = t_span / C
    c_per_bar = C / n
    print(f"[{c['split'][:5]}] {c['START'][11:16]}->{c['END'][11:16]} | {n:2d} | {dt:3d} | {C:3d} | {rng:6.2f} | {atr:5.2f} | {net:6.2f} | {C/dt:5.2f} | {ratio_m:6.2f} | {c_per_bar:5.2f}")
