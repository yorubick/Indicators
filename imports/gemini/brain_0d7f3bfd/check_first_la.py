import csv
from datetime import datetime, timezone

with open('G:/trading/guias/analisis/C_15s_start185530.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

for r in rows:
    if r['Layer A']:
        t = int(r['time'])
        dt_str = datetime.fromtimestamp(t, timezone.utc).strftime('%H:%M:%S')
        la = r['Layer A']
        lab = r['Layer A boundary']
        print(f"First Layer A at {dt_str}: Layer A = {la}, Layer A boundary = {lab}")
        break
