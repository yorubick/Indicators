import json
from pathlib import Path
import numpy as np

mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

print("=== TWO-PHASE EXPANSION VS CONSOLIDATION AUDIT ===")
print(f"{'START':<9} {'END':<9} {'B':<3} {'C':<6} {'State':<14} {'High':<9} {'Low':<9} {'NewHigh?':<9} {'NewLow?':<9}")

for c in sorted(cases, key=lambda x: (x['START'], x['END'])):
    if c['bars'] < 21: continue
    ohlc = c['OHLC']
    s = c['START']
    e = c['END']
    C = c['C']
    B = c['bars']
    
    highs = [float(r['high']) for r in ohlc]
    lows = [float(r['low']) for r in ohlc]
    
    # Check if last bar made a new high or low compared to preceding bars
    prev_high = max(highs[:-1])
    prev_low = min(lows[:-1])
    
    is_new_high = highs[-1] > prev_high
    is_new_low = lows[-1] < prev_low
    
    if is_new_high:
        state = "EXPANSION_UP"
    elif is_new_low:
        state = "EXPANSION_DOWN"
    else:
        state = "CONSOLIDATION"
        
    print(f"{s:<9} {e:<9} {B:<3d} {C:<6.1f} {state:<14} {highs[-1]:<9.2f} {lows[-1]:<9.2f} {str(is_new_high):<9} {str(is_new_low):<9}")
