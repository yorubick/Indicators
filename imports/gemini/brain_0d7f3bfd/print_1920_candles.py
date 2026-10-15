import csv, datetime
from pathlib import Path

ref_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(ref_path.open(encoding='utf-8-sig')))
candles = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

print("=== CANDLES AROUND 19:20 - 19:22 ===")
for t_str in [
    '19:18:00', '19:19:00',
    '19:20:00', '19:20:15', '19:20:30', '19:20:45',
    '19:21:00', '19:21:15', '19:21:30', '19:21:45',
    '19:22:00'
]:
    t = ts(t_str)
    if t in candles:
        c = candles[t]
        print(f"{t_str}: O={c['open']} H={c['high']} L={c['low']} C={c['close']}")
