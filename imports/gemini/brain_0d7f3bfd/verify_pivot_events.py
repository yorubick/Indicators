import json
from pathlib import Path

mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

def detect_pivot_events(ohlc):
    highs = [float(r['high']) for r in ohlc]
    lows = [float(r['low']) for r in ohlc]
    n = len(highs)
    
    # Candle n-2 is confirmed as pivot high by candle n-1 if high[n-2] >= high[n-3] and high[n-2] >= high[n-1]
    is_new_ph = False
    if n >= 3:
        if highs[-2] >= highs[-3] and highs[-2] >= highs[-1]:
            is_new_ph = True
            
    is_new_pl = False
    if n >= 3:
        if lows[-2] <= lows[-3] and lows[-2] <= lows[-1]:
            is_new_pl = True
            
    return is_new_ph, is_new_pl

print("=== PIVOT EVENT CORRELATION WITH C ===")
print(f"{'START':<9} {'END':<9} {'Bars':<5} {'C':<6} {'NewPH':<7} {'NewPL':<7} {'Notes'}")
prev_c = None
for c in sorted(cases, key=lambda x: (x['START'], x['END'])):
    if c['bars'] < 21: continue
    s = c['START']
    e = c['END']
    C = c['C']
    bars = c['bars']
    ohlc = c['OHLC']
    
    new_ph, new_pl = detect_pivot_events(ohlc)
    
    jump = ""
    if prev_c is not None and abs(C - prev_c) > 5:
        jump = f"<--- JUMP ({prev_c} -> {C})"
    prev_c = C
    
    print(f"{s:<9} {e:<9} {bars:<5d} {C:<6.1f} {str(new_ph):<7} {str(new_pl):<7} {jump}")
