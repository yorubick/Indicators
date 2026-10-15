import csv, datetime
from pathlib import Path

# Load 15s reference data
ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

# Test cases with known C
test_cases = [
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
]

for s_str, e_str, C in test_cases:
    target_pts = C * 0.25
    sub = [candles_15s[t] for t in range(ts(s_str), ts(e_str) + 15, 15) if t in candles_15s]
    # Check all price points
    found = []
    # Check if target_pts matches any price difference
    prices = []
    for i, b in enumerate(sub):
        for k in ('open', 'high', 'low', 'close'):
            prices.append((i, k, b[k]))
    
    # Check max difference in range
    h = max(b['high'] for b in sub)
    l = min(b['low'] for b in sub)
    total_range = h - l
    
    # Find closest pair difference to target_pts
    best_diff = 999
    best_pair = None
    for i in range(len(prices)):
        for j in range(i, len(prices)):
            diff = abs(prices[i][2] - prices[j][2])
            if abs(diff - target_pts) < abs(best_diff - target_pts):
                best_diff = diff
                best_pair = (prices[i], prices[j])
    
    print(f"START {s_str}: C={C} -> target={target_pts:.2f} pts (Total range={total_range:.2f} pts)")
    print(f"   Best pair diff: {best_diff:.2f} pts (err={best_diff - target_pts:.2f})")
