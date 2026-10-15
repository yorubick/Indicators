import json
from pathlib import Path

mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

def get_first_pivots(ohlc, strength=1):
    highs = [float(r['high']) for r in ohlc]
    lows = [float(r['low']) for r in ohlc]
    n = len(highs)
    
    first_ph = None
    for i in range(strength, n - strength):
        if all(highs[i] >= highs[i-k] for k in range(1, strength+1)) and all(highs[i] >= highs[i+k] for k in range(1, strength+1)):
            first_ph = (i, highs[i], ohlc[i]['time'])
            break
            
    first_pl = None
    for i in range(strength, n - strength):
        if all(lows[i] <= lows[i-k] for k in range(1, strength+1)) and all(lows[i] <= lows[i+k] for k in range(1, strength+1)):
            first_pl = (i, lows[i], ohlc[i]['time'])
            break
            
    return first_ph, first_pl

print("=== FIRST PIVOT ANALYSIS ACROSS ALL C_MATRIZ CASES ===")
print(f"{'START':<9} {'END':<9} {'Bars':<5} {'C':<6} {'1stPH_bar':<10} {'1stPH_price':<12} {'1stPL_bar':<10} {'1stPL_price':<12} {'1stSwingH':<10}")

for c in sorted(cases, key=lambda x: (x['START'], x['END'])):
    if c['bars'] < 21: continue
    s = c['START']
    e = c['END']
    C = c['C']
    B = c['bars']
    ohlc = c['OHLC']
    
    ph1, pl1 = get_first_pivots(ohlc, strength=1)
    
    ph1_bar = ph1[0] if ph1 else -1
    ph1_pr = ph1[1] if ph1 else 0
    pl1_bar = pl1[0] if pl1 else -1
    pl1_pr = pl1[1] if pl1 else 0
    
    swing1 = abs(ph1_pr - pl1_pr) if ph1 and pl1 else 0
    
    print(f"{s:<9} {e:<9} {B:<5d} {C:<6.1f} {ph1_bar:<10d} {ph1_pr:<12.2f} {pl1_bar:<10d} {pl1_pr:<12.2f} {swing1:<10.2f}")
