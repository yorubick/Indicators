import csv, datetime, math
from pathlib import Path
import numpy as np

# Load 15s reference data
ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

# Load 1m reference data
ref_1m_path = Path('G:/trading/guias/analisis/manual/Lite_0445_051500_1m_a.csv')
rows_1m = list(csv.DictReader(ref_1m_path.open(encoding='utf-8-sig')))
candles_1m = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_1m}

def ts(d_str, t_str):
    return int(datetime.datetime.fromisoformat(f"{d_str}T{t_str}+00:00").timestamp())

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

end_sweep_15s = [
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

def find_swings(sub, strength=1):
    n = len(sub)
    highs = [b['high'] for b in sub]
    lows = [b['low'] for b in sub]
    swings = []
    for i in range(strength, n - strength):
        is_h = all(highs[i] > highs[i - k] for k in range(1, strength + 1)) and \
               all(highs[i] > highs[i + k] for k in range(1, strength + 1))
        is_l = all(lows[i] < lows[i - k] for k in range(1, strength + 1)) and \
               all(lows[i] < lows[i + k] for k in range(1, strength + 1))
        if is_h:
            swings.append(('H', i, highs[i]))
        if is_l:
            swings.append(('L', i, lows[i]))
    return swings

print("=== Analyzing START sweep with swings (strength=1) ===")
t_end_15s = ts('2026-10-12', '19:20:00')

for s_str, C in start_sweep_15s:
    t_s = ts('2026-10-12', s_str)
    sub = [candles_15s[t] for t in range(t_s, t_end_15s + 15, 15) if t in candles_15s]
    swings = find_swings(sub, strength=1)
    
    # Let's filter alternating swings
    alt_swings = []
    for s in swings:
        if not alt_swings:
            alt_swings.append(s)
        elif alt_swings[-1][0] != s[0]:
            alt_swings.append(s)
        else: # Same type, keep more extreme
            if s[0] == 'H' and s[2] > alt_swings[-1][2]:
                alt_swings[-1] = s
            elif s[0] == 'L' and s[2] < alt_swings[-1][2]:
                alt_swings[-1] = s
                
    # Look for the first failure swing:
    # A High that is lower than previous High, or a Low that is higher than previous Low
    fs = None
    for i in range(2, len(alt_swings)):
        prev_same = [x for x in alt_swings[:i] if x[0] == alt_swings[i][0]]
        if prev_same:
            last_same = prev_same[-1]
            if alt_swings[i][0] == 'H' and alt_swings[i][2] < last_same[2]:
                fs = ('LH', alt_swings[i], last_same)
                break
            elif alt_swings[i][0] == 'L' and alt_swings[i][2] > last_same[2]:
                fs = ('HL', alt_swings[i], last_same)
                break
                
    n_bars = len(sub)
    if fs:
        fs_type, fs_swing, prev_swing = fs
        bars_to_end = n_bars - 1 - fs_swing[1]
        time_to_end = bars_to_end * 15
        price_diff = abs(fs_swing[2] - sub[-1]['close'])
        prev_move = abs(prev_swing[2] - sub[0]['open'])
        print(f"START {s_str} | C={C:3d} | FS={fs_type} at bar {fs_swing[1]:2d} ({fs_swing[2]:.2f}) | bars_to_end={bars_to_end:2d} ({time_to_end:4d}s) | P_diff={price_diff:5.2f}")
    else:
        print(f"START {s_str} | C={C:3d} | No Failure Swing found in {len(alt_swings)} swings")

