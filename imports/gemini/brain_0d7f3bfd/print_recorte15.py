import csv
from datetime import datetime, timezone

with open('G:/trading/guias/analisis/manual/C_recorte1903_15_c.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

for r in rows:
    t = int(r['time'])
    dt_str = datetime.fromtimestamp(t, timezone.utc).strftime('%H:%M:%S')
    if '19:23:00' <= dt_str <= '19:28:00':
        print(f"Time: {dt_str} | Close: {r.get('close')} | Lane 3 A: {r.get('Lane 3 A')} | Lane 3 B: {r.get('Lane 3 B')}")
