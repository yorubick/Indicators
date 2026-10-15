import json
from pathlib import Path
import numpy as np

mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

print("=== CHECKING TICKS AND BARS COMBINATIONS ON ALL N >= 21 ===")
print(f"{'START':<9} {'END':<9} {'B':<3} {'C':<6} {'R_pts':<6} {'Ticks':<6} {'T+B':<6} {'T-B':<6} {'2T-B':<6} {'Diff(C, T+B)':<12} {'Diff(C, T-B)':<12}")
for c in sorted(cases, key=lambda x: (x['START'], x['END'])):
    if c['bars'] < 21: continue
    s = c['START']
    e = c['END']
    C = c['C']
    B = c['bars']
    
    ohlc = c['OHLC']
    highs = [float(r['high']) for r in ohlc]
    lows = [float(r['low']) for r in ohlc]
    
    H = max(highs)
    L = min(lows)
    R = H - L
    T = round(R * 4)
    
    print(f"{s:<9} {e:<9} {B:<3d} {C:<6.1f} {R:<6.2f} {T:<6d} {T+B:<6d} {T-B:<6d} {2*T-B:<6d} {C-(T+B):<12.1f} {C-(T-B):<12.1f}")
