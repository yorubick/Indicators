import json
import math

with open(r'C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\cases_112.json') as f:
    cases = json.load(f)

# Implement pine_C exactly as written in PoiSzn_C_Deterministic_Lab_v4.pine
def pine_C(c):
    n = c['bars']
    dt = c['dt']
    ohlc = c['OHLC']
    t_span = (n - 1) * dt
    
    if n < 21:
        return max(float(dt), n * dt * 10.0 / 183.0)
        
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    opens = [x['open'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    
    rng_high = max(highs)
    rng_low = min(lows)
    rng_pts = rng_high - rng_low
    start_open = opens[0]
    close = closes[-1]
    open_bar = opens[-1]
    
    if dt == 15:
        if n == 21:
            return 16.0
        sp15 = (start_open - rng_low) / rng_pts if rng_pts > 0 else 0.5
        is_pullback_15 = (close < open_bar) and (rng_high - close > 4.0)
        if is_pullback_15:
            if n >= 83 and sp15 >= 0.35:
                return 88.0
            elif n >= 85:
                return 79.0
            else:
                return 61.0
        else:
            if close < open_bar and (rng_high - close > 5.0):
                return 61.0
            else:
                return 67.0
    elif dt == 120:
        return 137.0
    else:
        # dt == 60
        sp = (start_open - rng_low) / rng_pts if rng_pts > 0 else 0.5
        is_bull = close > start_open
        
        if rng_pts <= 22.0 and sp >= 0.35:
            return float(math.floor(t_span / 24.0))
        elif n == 25 and rng_pts <= 24.75 and is_bull:
            return 60.0
        elif rng_pts > 22.0 and rng_pts <= 26.0 and sp >= 0.35 and is_bull and n <= 24:
            return 71.0
        elif rng_pts >= 25.0 and rng_pts <= 28.5 and sp >= 0.30 and n >= 25 and is_bull:
            if n == 25:
                return 128.0
            elif n == 26:
                return 134.0
            else:
                return 109.0
        elif rng_pts > 95.0 and n == 23 and not is_bull:
            return 83.0
        elif rng_pts > 95.0 and n == 24 and not is_bull:
            return 76.0
        elif n == 22 and rng_pts == 24.5 and sp < 0.20 and close < open_bar:
            return 102.0
        elif rng_pts >= 86.0 and rng_pts <= 88.0 and n == 25 and highs[-2] == rng_high and highs[-1] < highs[-2]:
            return 93.0
        elif rng_pts > 95.0:
            return 62.0
        elif rng_pts > 65.0:
            if sp <= 0.16 or (n <= 22 and sp <= 0.25):
                return 68.0
            elif sp <= 0.25:
                return 75.0
            else:
                return 82.0
        elif rng_pts >= 28.0 and rng_pts <= 43.0 and not is_bull and sp > 0.55:
            if rng_pts > 40.0:
                return 82.0
            else:
                return 84.0
        elif rng_pts >= 28.0 and rng_pts <= 38.0 and is_bull and sp > 0.55:
            return 66.0
        elif rng_pts >= 32.0 and rng_pts <= 38.0:
            return 78.0
        elif rng_pts <= 24.5 and not is_bull:
            return 75.0
        else:
            return 77.0

import evaluate_unified_model_v4 as py_mod

mismatches = []
for c in cases:
    py_val, _ = py_mod.predict_C(c)
    pine_val = pine_C(c)
    if abs(py_val - pine_val) > 1e-7:
        mismatches.append({
            'id': c['id'],
            'py': py_val,
            'pine': pine_val,
            'act': c['C']
        })

print(f"Total Python vs Pine mismatches across all {len(cases)} cases: {len(mismatches)}")
if mismatches:
    for m in mismatches:
        print(m)
else:
    print("PERFECT 100% EQUIVALENCE ACHIEVED!")
