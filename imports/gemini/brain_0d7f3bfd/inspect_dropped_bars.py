import csv, datetime
from pathlib import Path

ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

start_times = [
    '18:54:00', '18:54:15', '18:54:30', '18:54:45',
    '18:55:00', '18:55:15', '18:55:30', '18:55:45',
    '18:56:00', '18:56:15', '18:56:30', '18:56:45', '18:57:00'
]
c_values = [123, 118, 67, 67, 106, 66, 88, 88, 106, 67, 67, 79, 67]

print(f"{'Start':<10} | {'C':>4} | {'Bar OHLC':<35} | Type")
print("-" * 65)
for i in range(len(start_times)):
    t = ts(start_times[i])
    c = candles[t]
    b_type = "BULL" if c['close'] > c['open'] else ("BEAR" if c['close'] < c['open'] else "DOJI")
    print(f"{start_times[i]:<10} | {c_values[i]:4d} | O={c['open']:.2f} H={c['high']:.2f} L={c['low']:.2f} C={c['close']:.2f} | {b_type}")
