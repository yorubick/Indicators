import csv
from datetime import datetime, timezone

with open(r'G:\trading\guias\analisis\seven_cloud_1m.csv') as f:
    rows = list(csv.DictReader(f))

print(f"Total rows: {len(rows)}")
print("Columns:", list(rows[0].keys())[:10])

# Print candles from 18:50 to 19:22
print("\nTime     | Open     | High     | Low      | Close    | Range | Dir")
print("-" * 65)
for r in rows:
    t_val = int(r['time'])
    dt_str = datetime.fromtimestamp(t_val, timezone.utc).strftime('%H:%M:%S')
    if '18:50:00' <= dt_str <= '19:22:00':
        o = float(r['open'])
        h = float(r['high'])
        l = float(r['low'])
        c = float(r['close'])
        rng = h - l
        d = "UP" if c >= o else "DN"
        print(f"{dt_str} | {o:8.2f} | {h:8.2f} | {l:8.2f} | {c:8.2f} | {rng:5.2f} | {d}")
