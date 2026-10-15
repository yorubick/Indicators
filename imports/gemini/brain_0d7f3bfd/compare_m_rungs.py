import json
import numpy as np

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

with open(r'G:\trading\guias\analisis\C_evolucion87_resultados.json') as f:
    data13 = json.load(f)

# Find the cases for m = 1, 2, 3, 4, 5
c_69 = next(c for c in data['cases'] if c['START'].startswith('2026-10-12T15:30') and c['bars'] == 21)
c_75 = next(c for c in data['cases'] if c['START'].startswith('2026-10-12T07:00') and c['bars'] == 21)
c_81 = next(c for c in data['cases'] if c['START'].startswith('2026-10-13T19:00') and c['bars'] == 21)
c_93 = next(c for c in data['cases'] if c['START'].startswith('2026-10-12T15:27') and c['bars'] == 25)

# For 87: from data13
with open(r'G:\trading\guias\analisis\C_evolucion87_predicciones.json') as f:
    p13 = json.load(f)
c_87_ohlc = p13['OHLC'][:21]

m_cases = [
    ('m=1 (C=69)', c_69['OHLC'], 69),
    ('m=2 (C=75)', c_75['OHLC'], 75),
    ('m=3 (C=81)', c_81['OHLC'], 81),
    ('m=4 (C=87)', c_87_ohlc, 87),
    ('m=5 (C=93)', c_93['OHLC'], 93),
]

print(f"{'Label':14s} | Bars | Range | ATR   | Net   | Path  | Rng/ATR | Path/Rng | Vol/Bars | Start_Pos")
print("-" * 90)
for label, ohlc, C in m_cases:
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    opens = [x['open'] for x in ohlc]
    
    n = len(ohlc)
    rng = max(highs) - min(lows)
    trs = [highs[0]-lows[0]] + [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, len(closes))]
    atr = np.mean(trs)
    net = closes[-1] - opens[0]
    path = sum(abs(closes[i] - closes[i-1]) for i in range(1, len(closes)))
    start_pos = (opens[0] - min(lows)) / rng if rng > 0 else 0.5
    
    print(f"{label:14s} | {n:4d} | {rng:5.2f} | {atr:5.2f} | {net:5.2f} | {path:5.2f} | {rng/atr:7.2f} | {path/rng:8.2f} | {path/n:8.2f} | {start_pos:9.2f}")
