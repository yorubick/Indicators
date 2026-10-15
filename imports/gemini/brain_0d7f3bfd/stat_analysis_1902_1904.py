import json
from pathlib import Path
import numpy as np

mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

print("=== DETAILED STATISTICAL ANALYSIS OF 19:02, 19:03, 19:04 RANGES ===")
target_cases = [c for c in cases if c['START'] in ('19:02:00', '19:03:00', '19:04:00') and c['END'] in ('19:22:00', '19:23:00', '19:24:00')]

for c in sorted(target_cases, key=lambda x: (x['bars'], x['START'])):
    ohlc = c['OHLC']
    s = c['START']
    e = c['END']
    C = c['C']
    B = c['bars']
    
    closes = np.array([float(r['close']) for r in ohlc])
    highs = np.array([float(r['high']) for r in ohlc])
    lows = np.array([float(r['low']) for r in ohlc])
    opens = np.array([float(r['open']) for r in ohlc])
    
    # TR
    tr = np.maximum(highs[1:] - lows[1:], np.maximum(np.abs(highs[1:] - closes[:-1]), np.abs(lows[1:] - closes[:-1])))
    atr = np.mean(tr)
    
    # Mean and std of candle ranges (high - low)
    bar_ranges = highs - lows
    mean_bar_rng = np.mean(bar_ranges)
    std_bar_rng = np.std(bar_ranges)
    
    # Total range
    R = np.max(highs) - np.min(lows)
    
    print(f"[{s} -> {e}] B={B} C={C:4.1f} | R={R:.2f} | ATR={atr:.4f} | MeanRng={mean_bar_rng:.4f} | StdRng={std_bar_rng:.4f} | CloseStd={np.std(closes):.4f}")
