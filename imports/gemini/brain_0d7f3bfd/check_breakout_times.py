import csv
from datetime import datetime, timezone

with open('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

by_time = {int(r['time']): {k: float(r[k]) for k in ('open', 'high', 'low', 'close')} for r in rows}

def ts(t_str):
    return int(datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

test_ranges = [
    ('18:54:00', '19:20:00'),
    ('18:55:00', '19:20:00'),
    ('19:00:00', '19:20:00'),
    ('19:03:00', '19:20:00'),
    ('19:03:15', '19:20:00'),
    ('19:03:00', '19:23:30'),
    ('19:03:15', '19:23:30'),
    ('19:03:30', '19:23:30'),
    ('19:03:00', '19:23:45'),
    ('19:03:15', '19:23:45'),
    ('19:03:30', '19:23:45')
]

for s_str, e_str in test_ranges:
    t_start, t_end = ts(s_str), ts(e_str)
    sub = [by_time[t] for t in range(t_start, t_end + 15, 15) if t in by_time]
    r_high = max(b['high'] for b in sub)
    r_low = min(b['low'] for b in sub)
    
    # Find breakout candle after t_end
    first_break = None
    for t in sorted(by_time.keys()):
        if t > t_end:
            b = by_time[t]
            if b['close'] > r_high or b['close'] < r_low:
                first_break = datetime.fromtimestamp(t, timezone.utc).strftime('%H:%M:%S')
                break_type = 'BULL' if b['close'] > r_high else 'BEAR'
                break
    print(f"START {s_str} - END {e_str} | High={r_high}, Low={r_low} | First Break: {first_break} ({break_type})")
