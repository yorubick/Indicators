import csv, datetime
from pathlib import Path

p = Path('G:/trading/guias/analisis/character_manual_15m_1m.csv')
rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

print("Time     | Open     | High     | Low      | Close    | High-Low | Close-Open")
for r in rows:
    t_val = int(r['time'])
    t_str = datetime.datetime.fromtimestamp(t_val, tz=datetime.timezone.utc).strftime('%H:%M:%S')
    if '18:50:00' <= t_str <= '19:05:00':
        o, h, l, c = float(r['open']), float(r['high']), float(r['low']), float(r['close'])
        print(f"{t_str} | {o:8.2f} | {h:8.2f} | {l:8.2f} | {c:8.2f} | {h-l:8.2f} | {c-o:10.2f}")
