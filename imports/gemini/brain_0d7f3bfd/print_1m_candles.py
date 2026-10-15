import csv, datetime
from pathlib import Path

p = Path('G:/trading/guias/analisis/manual/Lite_0445_051500_1m_a.csv')
rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))
candles = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

print("=== 1M CANDLES 18:50 - 19:05 ===")
for m in range(50, 60):
    t_str = f"18:{m:02d}:00"
    t = ts(t_str)
    if t in candles:
        c = candles[t]
        print(f"{t_str}: O={c['open']} H={c['high']} L={c['low']} C={c['close']}")

for m in range(0, 6):
    t_str = f"19:{m:02d}:00"
    t = ts(t_str)
    if t in candles:
        c = candles[t]
        print(f"{t_str}: O={c['open']} H={c['high']} L={c['low']} C={c['close']}")
