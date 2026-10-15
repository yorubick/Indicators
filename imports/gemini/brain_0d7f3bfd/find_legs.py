import csv, datetime
from pathlib import Path

ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

# Let's inspect the entire price path for 18:54:00 to 19:20:00
# and identify all legs: swing highs, swing lows, retracements
t_s = ts('18:54:00')
t_e = ts('19:20:00')
sub = [candles[t] for t in range(t_s, t_e + 15, 15) if t in candles]

print(f"Candles count: {len(sub)}")
# Let's identify the legs using 3-bar and 5-bar pivots
pivots = []
for i in range(1, len(sub)-1):
    if sub[i]['high'] > sub[i-1]['high'] and sub[i]['high'] > sub[i+1]['high']:
        pivots.append(('H', i, sub[i]['high'], datetime.datetime.fromtimestamp(t_s + i*15, datetime.timezone.utc).strftime('%H:%M:%S')))
    elif sub[i]['low'] < sub[i-1]['low'] and sub[i]['low'] < sub[i+1]['low']:
        pivots.append(('L', i, sub[i]['low'], datetime.datetime.fromtimestamp(t_s + i*15, datetime.timezone.utc).strftime('%H:%M:%S')))

print(f"Total pivots: {len(pivots)}")
for p in pivots[:15]:
    print(f"  {p[0]} at {p[3]} (bar {p[1]}): {p[2]:.2f}")
