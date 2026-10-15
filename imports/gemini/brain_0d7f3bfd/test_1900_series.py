import csv, datetime
from pathlib import Path
import numpy as np

# Load 1m data
p = Path('G:/trading/guias/analisis/character_manual_15m_1m.csv')
rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))

def stamp(s):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{s}:00+00:00").timestamp())

# Cases from 19:00
# 19:17 (18 bars) -> C = 60
# 19:18 (19 bars) -> C = 3800 / 61 = 62.29508197
# 19:19 (20 bars) -> C = 4000 / 61 = 65.57377049
# 19:20 (21 bars) -> C = 77.0

t_start = stamp('19:00')

print("=== EXACT OHLC FOR 19:00 to 19:20 (1m) ===")
bars_1900 = [r for r in rows if t_start <= int(r['time']) <= stamp('19:20')]

for i, b in enumerate(bars_1900):
    t_str = datetime.datetime.fromtimestamp(int(b['time']), tz=datetime.timezone.utc).strftime('%H:%M')
    o, h, l, c = float(b['open']), float(b['high']), float(b['low']), float(b['close'])
    print(f"Bar {i+1:2d} ({t_str}) | O={o:.2f} H={h:.2f} L={l:.2f} C={c:.2f} | H-L={h-l:5.2f} | C-O={c-o:6.2f}")
