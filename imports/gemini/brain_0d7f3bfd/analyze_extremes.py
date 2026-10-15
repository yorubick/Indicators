import csv, json, datetime
from pathlib import Path

# Load candles between 18:50 and 19:25 from the reference file
ref_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(ref_path.open(encoding='utf-8-sig')))

# Index by timestamp
candle_map = {}
for r in rows:
    candle_map[int(r['time'])] = {
        'open': float(r['open']),
        'high': float(r['high']),
        'low': float(r['low']),
        'close': float(r['close']),
        'volume': float(r.get('Volume', 0) or r.get('volume', 0))
    }

# Let's check the END sweep cases
end_cases = [
    ('18:55:00', '19:18:00', 88),
    ('18:55:00', '19:19:00', 115),
    ('18:55:00', '19:20:00', 106),
    ('18:55:00', '19:20:15', 79),
    ('18:55:00', '19:20:30', 67),
    ('18:55:00', '19:20:45', 66),
    ('18:55:00', '19:21:00', 115),
    ('18:55:00', '19:22:00', 106),
]

start_cases = [
    ('18:52:00', '19:20:00', 67),
    ('18:53:00', '19:20:00', 118),
    ('18:54:00', '19:20:00', 123),
    ('18:54:15', '19:20:00', 118),
    ('18:54:30', '19:20:00', 67),
    ('18:54:45', '19:20:00', 67),
    ('18:55:00', '19:20:00', 106),
    ('18:55:15', '19:20:00', 66),
    ('18:55:30', '19:20:00', 88),
    ('18:55:45', '19:20:00', 88),
    ('18:56:00', '19:20:00', 106),
    ('18:56:15', '19:20:00', 67),
    ('18:56:30', '19:20:00', 67),
    ('18:56:45', '19:20:00', 79),
    ('18:57:00', '19:20:00', 67),
    ('19:01:00', '19:20:00', 47),
    ('19:02:00', '19:20:00', 47),
]

def to_ts(time_str):
    return int(datetime.datetime.fromisoformat('2026-10-12T' + time_str + '+00:00').timestamp())

print("=== START SWEEP ANALYSIS ===")
for s_str, e_str, c in start_cases:
    ts_s = to_ts(s_str)
    ts_e = to_ts(e_str)
    sub = [candle_map[t] for t in range(ts_s, ts_e + 1, 15) if t in candle_map]
    highs = [x['high'] for x in sub]
    lows = [x['low'] for x in sub]
    max_h = max(highs)
    min_l = min(lows)
    height = max_h - min_l
    first_c = sub[0]
    last_c = sub[-1]
    
    # Let's find index of max_h and min_l
    idx_max = highs.index(max_h)
    idx_min = lows.index(min_l)
    t_max = ts_s + idx_max * 15
    t_min = ts_s + idx_min * 15
    
    print(f"START {s_str} | C={c:3d} | H={max_h:.2f}(@{idx_max:2d}) L={min_l:.2f}(@{idx_min:2d}) Height={height:.2f} | End-H={len(sub)-1-idx_max} End-L={len(sub)-1-idx_min}")
