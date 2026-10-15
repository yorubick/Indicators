import csv, datetime
from pathlib import Path

ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

start_cases = [
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

print("Evaluating pivots within truncated [START, END] ranges:")
for left in [1, 2]:
    for right in [1, 2]:
        print(f"\n=== Pivots with left={left}, right={right} ===")
        for s_str, C in start_cases:
            t_s = ts(s_str)
            sub = [candles[t] for t in range(t_s, t_end + 15, 15) if t in candles]
            highs = [b['high'] for b in sub]
            lows = [b['low'] for b in sub]
            
            # Find first pivot high and first pivot low
            p_highs = []
            p_lows = []
            for i in range(left, len(sub) - right):
                if all(highs[i] > highs[i-k] for k in range(1, left+1)) and all(highs[i] > highs[i+k] for k in range(1, right+1)):
                    p_highs.append(i)
                if all(lows[i] < lows[i-k] for k in range(1, left+1)) and all(lows[i] < lows[i+k] for k in range(1, right+1)):
                    p_lows.append(i)
            
            first_h = p_highs[0] if p_highs else -1
            first_l = p_lows[0] if p_lows else -1
            print(f"START {s_str}: C={C:3d} | first_PH_idx={first_h:2d} (bar {first_h}), first_PL_idx={first_l:2d}")
