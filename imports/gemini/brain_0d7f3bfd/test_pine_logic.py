import csv, json
from datetime import datetime, timezone
from pathlib import Path

cases_to_test = [
    {
        'file': 'G:/trading/guias/analisis/manual/Lite_1855_1920_1m_b.csv',
        'start': '2026-10-12T18:55:00Z',
        'end': '2026-10-12T19:20:00Z',
        'dt': 60,
        'C': 62.0,
        'name': 'Alcista 1m C62'
    },
    {
        'file': 'G:/trading/guias/analisis/manual/Lite_185415_1920_15s_a.csv',
        'start': '2026-10-12T18:54:15Z',
        'end': '2026-10-12T19:20:00Z',
        'dt': 15,
        'C': 118.0,
        'name': 'Alcista 15s C118'
    },
    {
        'file': 'G:/trading/guias/analisis/manual/Lite_0445_053000_1m_a.csv',
        'start': '2026-10-12T04:45:00Z',
        'end': '2026-10-12T05:30:00Z',
        'dt': 60,
        'C': 110.0,
        'name': 'Bajista 1m C110'
    }
]

def stamp(s):
    return int(datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp())

lanes = ['Lane 3 A', 'Lane 3 B', 'Lane 2 A', 'Lane 2 B', 'Lane 1 A', 'Lane 1 B']
bases = [72/3, 89/3, 72/9, 89/9, 72/27, 89/27]

print("=== TESTING EXACT RECONSTRUCTION LOGIC ===")
for c in cases_to_test:
    rows = list(csv.DictReader(open(c['file'], encoding='utf-8-sig')))
    t_start = stamp(c['start'])
    t_end = stamp(c['end'])
    dt = c['dt']
    C = c['C']
    
    # 1. Range bounds
    selected = [r for r in rows if t_start <= int(r['time']) <= t_end]
    rng_high = max(float(r['high']) for r in selected)
    rng_low = min(float(r['low']) for r in selected)
    end_row = next(r for r in selected if int(r['time']) == t_end)
    end_low = float(end_row['low'])
    end_high = float(end_row['high'])
    
    # 2. Periods
    periods = [base * C / dt for base in bases]
    alphas = [2.0 / (N + 1.0) for N in periods]
    
    # 3. State initialization at END
    state_bull = [end_low] * 6
    state_bear = [end_high] * 6
    side = None
    
    post_bars = [r for r in rows if int(r['time']) > t_end]
    errors = []
    premature = 0
    mismatch_visibility = 0
    
    for r in post_bars:
        t = int(r['time'])
        close = float(r['close'])
        
        # Immediate update on every bar after END
        state_bull = [s + a * (close - s) for s, a in zip(state_bull, alphas)]
        state_bear = [s + a * (close - s) for s, a in zip(state_bear, alphas)]
        
        # Check breakout
        if side is None:
            if close > rng_high:
                side = 'bull'
            elif close < rng_low:
                side = 'bear'
                
        active_state = state_bull if side == 'bull' else (state_bear if side == 'bear' else None)
        
        for i, lane in enumerate(lanes):
            orig_str = r.get(lane, '')
            orig_val = float(orig_str) if orig_str != '' else None
            
            if orig_val is not None:
                if active_state is None:
                    mismatch_visibility += 1
                else:
                    errors.append(abs(active_state[i] - orig_val))
            else:
                if active_state is not None:
                    premature += 1
                    
    max_err = max(errors) if errors else 0.0
    print(f"{c['name']:16s} | Compared: {len(errors):5d} | Max Err: {max_err:12.6e} | Premature: {premature:2d} | Mismatch: {mismatch_visibility:2d}")
