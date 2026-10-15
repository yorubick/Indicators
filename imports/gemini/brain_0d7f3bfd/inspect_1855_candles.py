import csv
from pathlib import Path
from datetime import datetime, timezone

ref_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_path.open(encoding='utf-8-sig')))

print(f"{'Time UTC':<20} {'Open':<10} {'High':<10} {'Low':<10} {'Close':<10} {'Range':<8}")
for r in rows_15s:
    t = int(r['time'])
    dt = datetime.fromtimestamp(t, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    if '18:53:30' <= dt[11:] <= '18:57:30':
        o, h, l, c = float(r['open']), float(r['high']), float(r['low']), float(r['close'])
        print(f"{dt:<20} {o:<10.2f} {h:<10.2f} {l:<10.2f} {c:<10.2f} {h-l:<8.2f}")
