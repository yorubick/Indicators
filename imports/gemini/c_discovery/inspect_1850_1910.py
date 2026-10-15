import csv

csv_path = r"G:\trading\guias\analisis\manual\Lite_1903_192300_1m_b.csv"
rows = {}
with open(csv_path, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows[int(r["time"])] = r

sorted_times = sorted(rows.keys())

# Let's inspect candles 18:50 to 19:10
import datetime
for t in sorted_times:
    dt = datetime.datetime.fromtimestamp(t, datetime.timezone.utc)
    if "2026-10-12" in str(dt) and "18:50" <= dt.strftime("%H:%M") <= "19:10":
        r = rows[t]
        print(f"{dt.strftime('%H:%M')} | O={float(r['open']):8.2f} H={float(r['high']):8.2f} L={float(r['low']):8.2f} C={float(r['close']):8.2f}")
