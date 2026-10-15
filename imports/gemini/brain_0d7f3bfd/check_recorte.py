import csv, glob
from datetime import datetime, timezone

for p in glob.glob('G:/trading/guias/analisis/manual/C_recorte1903_*.csv'):
    with open(p, encoding='utf-8-sig') as f:
        r = list(csv.DictReader(f))
        for row in r:
            t = int(row.get('time', 0))
            dt_str = datetime.fromtimestamp(t, timezone.utc).strftime('%H:%M:%S')
            if dt_str == '19:26:45':
                l3a = row.get('Lane 3 A', '')
                l3b = row.get('Lane 3 B', '')
                print(f"{p} at 19:26:45: Lane 3 A = {l3a}, Lane 3 B = {l3b}")
