import csv
from datetime import datetime, timezone

with open('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv', encoding='utf-8-sig') as f:
    r = list(csv.DictReader(f))

for row in r:
    t = int(row['time'])
    dt_str = datetime.fromtimestamp(t, timezone.utc).strftime('%H:%M:%S')
    if '19:20:00' <= dt_str <= '19:28:00':
        print(f"{dt_str} | O={row['open']} H={row['high']} L={row['low']} C={row['close']}")
