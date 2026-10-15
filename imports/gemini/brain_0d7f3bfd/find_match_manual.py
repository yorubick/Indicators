import csv, glob
from datetime import datetime, timezone

target_a = '30866.77'
target_b = '30866.63'

for p in glob.glob('G:/trading/guias/analisis/manual/*.csv'):
    with open(p, encoding='utf-8-sig') as f:
        r = list(csv.DictReader(f))
        for row in r:
            t = int(row.get('time', 0))
            dt_str = datetime.fromtimestamp(t, timezone.utc).strftime('%H:%M:%S')
            if dt_str == '19:26:45':
                l3a = row.get('Lane 3 A', '')
                l3b = row.get('Lane 3 B', '')
                if '30866.7' in l3a or '30866.6' in l3b:
                    print(f"MATCH FOUND in {p}: Lane 3 A = {l3a}, Lane 3 B = {l3b}")
