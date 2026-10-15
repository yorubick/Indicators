import csv, datetime
from pathlib import Path

p = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

# Find the row at 19:26:45
target_ts = ts('19:26:45')
print("Target ts:", target_ts)

# Let's see rows from 19:23:00 to 19:27:00
recent = [r for r in rows if ts('19:23:00') <= int(r['time']) <= ts('19:27:00')]
print(f"Found {len(recent)} rows around 19:23 - 19:27")
for r in recent:
    t_iso = datetime.datetime.fromtimestamp(int(r['time']), datetime.timezone.utc).strftime('%H:%M:%S')
    print(f"{t_iso} ({r['time']}): O={r['open']}, H={r['high']}, L={r['low']}, C={r['close']}")
