import csv, datetime
from pathlib import Path

ref_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(ref_path.open(encoding='utf-8-sig')))
for r in rows:
    t = int(r['time'])
    dt = datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime('%H:%M:%S')
    if '18:54:00' <= dt <= '18:57:30':
        print(f"{dt}: O={float(r['open']):.2f} H={float(r['high']):.2f} L={float(r['low']):.2f} C={float(r['close']):.2f}")
