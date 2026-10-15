import csv
from datetime import datetime, timezone

with open('G:/trading/guias/analisis/manual/C_cruce1903_15_d.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

print(f"Total rows in C_cruce1903_15_d.csv: {len(rows)}")
for r in rows:
    t = int(r['time'])
    dt_str = datetime.fromtimestamp(t, timezone.utc).strftime('%H:%M:%S')
    if dt_str in ['19:23:30', '19:23:45', '19:26:45', '19:27:00']:
        l3a = r.get('Lane 3 A')
        l3b = r.get('Lane 3 B')
        cl = r.get('close')
        print(f"Time: {dt_str} | Close: {cl} | Lane 3 A: {l3a} | Lane 3 B: {l3b}")
