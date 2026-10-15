import csv, datetime
from pathlib import Path

ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

t_start = ts('18:54:00')
t_end = ts('19:20:00')
bars = []
for t in range(t_start, t_end + 15, 15):
    if t in candles:
        c = candles[t]
        dt = datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime('%H:%M:%S')
        bars.append({'t': t, 'dt': dt, 'o': c['open'], 'h': c['high'], 'l': c['low'], 'c': c['close']})

print(f"Total bars from 18:54:00 to 19:20:00: {len(bars)}")

# Find swing highs and lows with left=1, right=1 (3-bar fractal)
print("\n--- 3-bar Pivots (left=1, right=1) ---")
for i in range(1, len(bars) - 1):
    if bars[i]['h'] > bars[i-1]['h'] and bars[i]['h'] > bars[i+1]['h']:
        print(f"Pivot High at {bars[i]['dt']} (bar {i}): H={bars[i]['h']:.2f}")
    if bars[i]['l'] < bars[i-1]['l'] and bars[i]['l'] < bars[i+1]['l']:
        print(f"Pivot Low at {bars[i]['dt']} (bar {i}): L={bars[i]['l']:.2f}")

# Find swing highs and lows with left=2, right=2 (5-bar fractal)
print("\n--- 5-bar Pivots (left=2, right=2) ---")
for i in range(2, len(bars) - 2):
    if all(bars[i]['h'] > bars[i+k]['h'] for k in [-2, -1, 1, 2]):
        print(f"Major High at {bars[i]['dt']} (bar {i}): H={bars[i]['h']:.2f}")
    if all(bars[i]['l'] < bars[i+k]['l'] for k in [-2, -1, 1, 2]):
        print(f"Major Low at {bars[i]['dt']} (bar {i}): L={bars[i]['l']:.2f}")
