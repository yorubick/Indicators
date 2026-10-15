import json
from pathlib import Path
import numpy as np

matriz_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
data = json.loads(matriz_path.read_text(encoding='utf-8'))

# Let's inspect each case with its full candle series
print("=== DETAILED MATRIX ANALYSIS ===")
for c in sorted(data['cases'], key=lambda x: (x['START'], x['END'])):
    ohlc = c['OHLC']
    s = c['START']
    e = c['END']
    C = c['C']
    bars = c['bars']
    
    # Calculate various candidate metrics on the selected range:
    highs = [float(r['high']) for r in ohlc]
    lows = [float(r['low']) for r in ohlc]
    closes = [float(r['close']) for r in ohlc]
    opens = [float(r['open']) for r in ohlc]
    volumes = [float(r.get('volume', 0)) for r in ohlc]
    
    rng = max(highs) - min(lows)
    h_idx = highs.index(max(highs)) # index from start
    l_idx = lows.index(min(lows))
    
    # distance from end
    bars_from_high = bars - 1 - h_idx
    bars_from_low = bars - 1 - l_idx
    
    # total path length (sum of abs(diff(close))) or sum of true ranges
    tr_sum = sum(max(h - l, abs(h - c_prev), abs(l - c_prev)) for h, l, c_prev in zip(highs[1:], lows[1:], closes[:-1]))
    abs_move = abs(closes[-1] - opens[0])
    eff = abs_move / tr_sum if tr_sum > 0 else 0
    
    # Volume weighted or tick count?
    ticks = sum(float(r.get('ticks', 0)) for r in ohlc)
    
    print(f"[{s} -> {e}] B={bars:2d} C={C:6.2f} | Rng={rng:5.2f} | H_idx={h_idx:2d} ({-bars_from_high:2d}) L_idx={l_idx:2d} ({-bars_from_low:2d}) | TR_sum={tr_sum:5.2f} | AbsM={abs_move:5.2f} | C/B={C/bars:5.2f}")
