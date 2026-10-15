import csv, datetime
from pathlib import Path

ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

start_sweep_15s = [
    ('18:54:00', 123),
    ('18:54:15', 118),
    ('18:54:30', 67),
    ('18:54:45', 67),
    ('18:55:00', 106),
    ('18:55:15', 66),
    ('18:55:30', 88),
    ('18:55:45', 88),
    ('18:56:00', 106),
    ('18:56:15', 67),
    ('18:56:30', 67),
    ('18:56:45', 79),
    ('18:57:00', 67),
]

t_end = ts('19:20:00')

print("Detailed leg structure from START candle forward:")
for s_str, C in start_sweep_15s:
    t_s = ts(s_str)
    sub = [candles_15s[t] for t in range(t_s, t_end + 15, 15) if t in candles_15s]
    
    # First 10 bars
    print(f"\n--- START {s_str} (C={C}) ---")
    for i in range(min(8, len(sub))):
        b = sub[i]
        dt = datetime.datetime.fromtimestamp(t_s + i*15, datetime.timezone.utc).strftime('%H:%M:%S')
        print(f"  Bar {i:2d} ({dt}): O={b['open']:.2f} H={b['high']:.2f} L={b['low']:.2f} C={b['close']:.2f}")
