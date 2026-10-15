import json
from pathlib import Path

mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

print("=== TESTING TICK DISPLACEMENTS ===")
print(f"{'START':<9} {'END':<9} {'Bars':<5} {'C':<6} {'R_pts':<6} {'Ticks':<6} {'Net_pts':<8} {'NetTicks':<9} {'Ticks-B':<8} {'NetT-B':<8} {'Close-L':<8}")
for c in sorted(cases, key=lambda x: (x['START'], x['END'])):
    ohlc = c['OHLC']
    s = c['START']
    e = c['END']
    C = c['C']
    bars = c['bars']
    
    highs = [float(r['high']) for r in ohlc]
    lows = [float(r['low']) for r in ohlc]
    closes = [float(r['close']) for r in ohlc]
    opens = [float(r['open']) for r in ohlc]
    
    H = max(highs)
    L = min(lows)
    R = H - L
    ticks = round(R * 4)
    
    net_pts = abs(closes[-1] - opens[0])
    net_ticks = round(net_pts * 4)
    
    move_from_low = abs(closes[-1] - L)
    ticks_from_low = round(move_from_low * 4)
    
    print(f"{s:<9} {e:<9} {bars:<5d} {C:<6.1f} {R:<6.2f} {ticks:<6d} {net_pts:<8.2f} {net_ticks:<9d} {ticks-bars:<8d} {net_ticks-bars:<8d} {ticks_from_low:<8d}")
