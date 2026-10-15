import csv, json, datetime
from pathlib import Path
import numpy as np

# Load 15s and 1m reference data
ref_15s = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

ref_1m = Path('G:/trading/guias/analisis/character_manual_15m_1m.csv')
rows_1m = list(csv.DictReader(ref_1m.open(encoding='utf-8-sig')))
candles_1m = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_1m}

def ts(d, t):
    return int(datetime.datetime.fromisoformat(f"{d}T{t}+00:00").timestamp())

# Import the dataset from master_cases
import sys
sys.path.insert(0, 'C:/Users/PC/.gemini/antigravity/brain/0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27/scratch')
from master_cases import cases

print("=== BREAKOUT ANALYSIS (POST-END DATA) ===")
results = []

for date, s, e, dt, C, c_map in cases:
    t_s = ts(date, s)
    t_e = ts(date, e)
    
    # Range bars
    range_bars = [c_map[t] for t in range(t_s, t_e + 1, dt) if t in c_map]
    if not range_bars: continue
    
    box_high = max(x['high'] for x in range_bars)
    box_low = min(x['low'] for x in range_bars)
    
    # Search for breakout after t_e
    # Look forward up to 2 hours
    t_max_search = t_e + 7200
    breakout_t = None
    breakout_type = None
    breakout_bar = None
    
    for t in range(t_e + dt, t_max_search + 1, dt):
        if t in c_map:
            bar = c_map[t]
            if bar['close'] > box_high:
                breakout_t = t
                breakout_type = 'BULL'
                breakout_bar = bar
                break
            elif bar['close'] < box_low:
                breakout_t = t
                breakout_type = 'BEAR'
                breakout_bar = bar
                break
                
    if breakout_t:
        bars_to_breakout = (breakout_t - t_e) // dt
        seconds_to_breakout = breakout_t - t_e
        breakout_dist_from_start = breakout_t - t_s
        penetration = (breakout_bar['close'] - box_high) if breakout_type == 'BULL' else (box_low - breakout_bar['close'])
        
        results.append({
            'date': date, 's': s, 'e': e, 'dt': dt, 'C': C,
            'box_h': box_high, 'box_l': box_low,
            'brk_type': breakout_type,
            'brk_time': datetime.datetime.fromtimestamp(breakout_t, datetime.timezone.utc).strftime('%H:%M:%S'),
            's_to_brk': seconds_to_breakout,
            'bars_to_brk': bars_to_breakout,
            'penetration': penetration,
            'brk_close': breakout_bar['close'],
            'total_dist': breakout_dist_from_start
        })

print(f"{'START':8s} {'END':8s} {'dt':2s} | {'C':4s} | {'Box H':8s} {'Box L':8s} | {'Breakout':8s} {'Type':4s} | {'Sec to Brk':10s} {'Penetration':11s}")
for r in results:
    print(f"{r['s']:8s} {r['e']:8s} {r['dt']:2d} | {r['C']:4d} | {r['box_h']:8.2f} {r['box_l']:8.2f} | {r['brk_time']:8s} {r['brk_type']:4s} | {r['s_to_brk']:10d} {r['penetration']:11.2f}")
