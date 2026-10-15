import json
from pathlib import Path

matriz_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
data = json.loads(matriz_path.read_text(encoding='utf-8'))

# Grab one case that contains all candles up to 19:30
case_1904_30 = next(c for c in data['cases'] if c['START'] == '19:04:00' and c['END'] == '19:30:00')
case_1900_24 = next(c for c in data['cases'] if c['START'] == '19:00:00' and c['END'] == '19:24:00')

# Merge candles to get full 19:00 to 19:30
all_candles = {}
for r in case_1900_24['OHLC']:
    all_candles[int(r['time'])] = r
for r in case_1904_30['OHLC']:
    all_candles[int(r['time'])] = r

from datetime import datetime, timezone
print(f"{'Time':<10} {'Open':<10} {'High':<10} {'Low':<10} {'Close':<10} {'Range':<8} {'Body':<8} {'Color':<6}")
for t in sorted(all_candles.keys()):
    dt = datetime.fromtimestamp(t, timezone.utc).strftime('%H:%M:%S')
    r = all_candles[t]
    o, h, l, c = float(r['open']), float(r['high']), float(r['low']), float(r['close'])
    rng = h - l
    body = c - o
    color = "GREEN" if c >= o else "RED"
    print(f"{dt:<10} {o:<10.2f} {h:<10.2f} {l:<10.2f} {c:<10.2f} {rng:<8.2f} {body:<8.2f} {color:<6}")
