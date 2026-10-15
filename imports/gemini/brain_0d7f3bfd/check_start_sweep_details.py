import csv, datetime
from pathlib import Path

p = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

c_map = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows}

start_cases = [
    ('18:52:00', 67),
    ('18:53:00', 118),
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
    ('19:01:00', 47),
    ('19:02:00', 47),
]

end_ts = ts('19:20:00')

print("END: 19:20:00")
print("START    | C   | Bars | Range | High     | Low      | Start Bar OHLC                             | Start High-Low | Start Close-Open")
for s_str, C in start_cases:
    s_ts = ts(s_str)
    sub = [c_map[t] for t in range(s_ts, end_ts + 15, 15) if t in c_map]
    highs = [b['high'] for b in sub]
    lows = [b['low'] for b in sub]
    sb = sub[0]
    rng = max(highs) - min(lows)
    
    print(f"{s_str} | {C:3d} | {len(sub):4d} | {rng:5.2f} | {max(highs):8.2f} | {min(lows):8.2f} | O={sb['open']:.2f} H={sb['high']:.2f} L={sb['low']:.2f} C={sb['close']:.2f} | {sb['high']-sb['low']:5.2f} | {sb['close']-sb['open']:6.2f}")
