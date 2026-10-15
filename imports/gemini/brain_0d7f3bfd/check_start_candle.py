import json
from pathlib import Path

mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

print("=== START CANDLE PROPERTIES VS C ===")
print(f"{'START':<9} {'END':<9} {'Bars':<5} {'C':<6} {'StartColor':<11} {'StartOpen':<10} {'StartHigh':<10} {'StartLow':<10} {'StartClose':<10} {'StartBody':<10}")

for c in sorted(cases, key=lambda x: (x['START'], x['END'])):
    if c['bars'] < 21: continue
    s = c['START']
    e = c['END']
    C = c['C']
    B = c['bars']
    ohlc = c['OHLC']
    
    first = ohlc[0]
    o, h, l, cl = float(first['open']), float(first['high']), float(first['low']), float(first['close'])
    color = "GREEN (UP)" if cl >= o else "RED (DOWN)"
    body = cl - o
    
    print(f"{s:<9} {e:<9} {B:<5d} {C:<6.1f} {color:<11} {o:<10.2f} {h:<10.2f} {l:<10.2f} {cl:<10.2f} {body:<10.2f}")
