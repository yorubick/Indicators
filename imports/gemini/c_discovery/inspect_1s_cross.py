import csv

path_a = r"G:\trading\guias\analisis\manual\C_1s_salida_140401_140433_a.csv"
path_b = r"G:\trading\guias\analisis\manual\C_1s_salida_140400_140432_a.csv"

# Let's inspect rows around 14:04:00 and 14:04:33
rows = {}
with open(path_a, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows[int(r["time"])] = r

with open(path_b, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows[int(r["time"])] = r

import datetime
for t in sorted(rows.keys()):
    dt = datetime.datetime.fromtimestamp(t, datetime.timezone.utc)
    if "14:04:00" <= dt.strftime("%H:%M:%S") <= "14:04:35":
        r = rows[t]
        print(f"{dt.strftime('%H:%M:%S')} | O={float(r['open']):.2f} H={float(r['high']):.2f} L={float(r['low']):.2f} C={float(r['close']):.2f} V={float(r['Volume'])}")
