import csv, datetime
from pathlib import Path

p = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

c_map = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows}

end_cases = [
    ('19:18:00', 88),
    ('19:19:00', 115),
    ('19:20:00', 106),
    ('19:20:15', 79),
    ('19:20:30', 67),
    ('19:20:45', 66),
    ('19:21:00', 115),
    ('19:21:15', 106),
    ('19:21:30', 79),
    ('19:21:45', 66),
    ('19:22:00', 106),
]

start_ts = ts('18:55:00')

print("START: 18:55:00")
print("END      | C   | Bars | Range | High     | Low      | End Bar OHLC                               | Max - C | Bars since High")
for end_str, C in end_cases:
    end_ts = ts(end_str)
    sub = [c_map[t] for t in range(start_ts, end_ts + 15, 15) if t in c_map]
    highs = [b['high'] for b in sub]
    lows = [b['low'] for b in sub]
    end_bar = sub[-1]
    rng = max(highs) - min(lows)
    max_c = max(highs) - end_bar['close']
    
    # Find last bar index with high == max(highs)
    last_high_idx = max(i for i, b in enumerate(sub) if b['high'] == max(highs))
    bars_since_high = len(sub) - 1 - last_high_idx
    
    bo = end_bar['open']
    bh = end_bar['high']
    bl = end_bar['low']
    bc = end_bar['close']
    print(f"{end_str} | {C:3d} | {len(sub):4d} | {rng:5.2f} | {max(highs):8.2f} | {min(lows):8.2f} | O={bo:.2f} H={bh:.2f} L={bl:.2f} C={bc:.2f} | {max_c:7.2f} | {bars_since_high:2d}")
