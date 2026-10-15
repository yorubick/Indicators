import csv, datetime
from pathlib import Path

p = Path('G:/trading/guias/analisis/manual/Lite_0445_051500_1m_a.csv')
rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))

print("=== Morning 1m Candles from 05:10 to 05:35 ===")
for r in rows:
    t_val = int(r['time'])
    t_str = datetime.datetime.fromtimestamp(t_val, tz=datetime.timezone.utc).strftime('%H:%M:%S')
    if '05:10:00' <= t_str <= '05:35:00':
        o, h, l, c = float(r['open']), float(r['high']), float(r['low']), float(r['close'])
        print(f"{t_str} | O={o:8.2f} H={h:8.2f} L={l:8.2f} C={c:8.2f} | Range={h-l:5.2f} | Close-Low={c-l:5.2f}")
