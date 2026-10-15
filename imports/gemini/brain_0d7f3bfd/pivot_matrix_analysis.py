import json
from pathlib import Path
import numpy as np

mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

def find_pivots(highs, lows, strength=1):
    n = len(highs)
    ph = []
    pl = []
    for i in range(strength, n - strength):
        if all(highs[i] >= highs[i-k] for k in range(1, strength+1)) and all(highs[i] >= highs[i+k] for k in range(1, strength+1)):
            ph.append((i, highs[i]))
        if all(lows[i] <= lows[i-k] for k in range(1, strength+1)) and all(lows[i] <= lows[i+k] for k in range(1, strength+1)):
            pl.append((i, lows[i]))
    return ph, pl

print("=== PIVOT AND SWING STRUCTURE ANALYSIS ON 1M MATRIZ ===")
print(f"{'START':<9} {'END':<9} {'B':<3} {'C':<5} {'PH_count':<9} {'PL_count':<9} {'LastPH_bar':<11} {'LastPL_bar':<11} {'LastPH_val':<11} {'LastPL_val':<11} {'SwingHeight':<11}")
for c in sorted(cases, key=lambda x: (x['START'], x['END'])):
    if c['bars'] < 21: continue
    ohlc = c['OHLC']
    highs = [float(r['high']) for r in ohlc]
    lows = [float(r['low']) for r in ohlc]
    
    ph, pl = find_pivots(highs, lows, strength=1)
    
    last_ph = ph[-1] if ph else (-1, 0)
    last_pl = pl[-1] if pl else (-1, 0)
    
    # height between last PH and last PL
    swing_h = abs(last_ph[1] - last_pl[1]) if ph and pl else 0
    
    print(f"{c['START']:<9} {c['END']:<9} {c['bars']:<3d} {c['C']:<5.1f} {len(ph):<9d} {len(pl):<9d} {last_ph[0]:<11d} {last_pl[0]:<11d} {last_ph[1]:<11.2f} {last_pl[1]:<11.2f} {swing_h:<11.2f}")
