import csv, datetime
from pathlib import Path

ref_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(ref_path.open(encoding='utf-8-sig')))

# Let's inspect the columns in the CSV
print("Columns in CSV:", rows[0].keys())

# Let's inspect candles from 18:52:00 to 18:58:00
for r in rows:
    t = datetime.datetime.fromtimestamp(int(r['time']), datetime.timezone.utc)
    t_str = t.strftime('%H:%M:%S')
    if '18:52:00' <= t_str <= '18:58:00':
        print(f"{t_str} | O:{float(r['open']):8.2f} H:{float(r['high']):8.2f} L:{float(r['low']):8.2f} C:{float(r['close']):8.2f} | " + 
              " ".join(f"{k}:{r[k]}" for k in r if k not in ('time','open','high','low','close') and r[k] != ''))
