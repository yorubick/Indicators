import json
from pathlib import Path

mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

print("=== START POSITION VS FIBONACCI RATIO ===")
print(f"{'START':<9} {'END':<9} {'Bars':<5} {'C':<6} {'StartPos':<10} {'EndPos':<10} {'NetMove':<10} {'Ticks':<6} {'C/Ticks':<8}")

for c in sorted(cases, key=lambda x: (x['START'], x['END'])):
    if c['bars'] < 21: continue
    s = c['START']
    e = c['END']
    C = c['C']
    B = c['bars']
    
    ohlc = c['OHLC']
    highs = [float(r['high']) for r in ohlc]
    lows = [float(r['low']) for r in ohlc]
    closes = [float(r['close']) for r in ohlc]
    opens = [float(r['open']) for r in ohlc]
    
    H = max(highs)
    L = min(lows)
    R = H - L
    T = round(R * 4)
    
    start_pos = (opens[0] - L) / R
    end_pos = (closes[-1] - L) / R
    net_move = (closes[-1] - opens[0]) / R
    
    c_ratio = C / T
    
    print(f"{s:<9} {e:<9} {B:<5d} {C:<6.1f} {start_pos:<10.3f} {end_pos:<10.3f} {net_move:<10.3f} {T:<6d} {c_ratio:<8.3f}")
