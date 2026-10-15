import csv, json, datetime
from pathlib import Path
import numpy as np

# Load reference candles
ref_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(ref_path.open(encoding='utf-8-sig')))

candle_map = {}
for r in rows:
    candle_map[int(r['time'])] = {
        'open': float(r['open']),
        'high': float(r['high']),
        'low': float(r['low']),
        'close': float(r['close']),
    }

barrido = json.load(open('G:/trading/guias/analisis/C_barrido_ampliado.json', encoding='utf-8'))

def to_ts(time_str):
    return int(datetime.datetime.fromisoformat('2026-10-12T' + time_str + '+00:00').timestamp())

print("=== ICT STRUCTURE / CHOCH EXPLORATION ===")
for c in barrido['cases']:
    s_str = c['START_UTC']
    ts_s = to_ts(s_str)
    ts_e = to_ts('19:20:00')
    dt = 15
    sub = [(t, candle_map[t]) for t in range(ts_s, ts_e + 1, dt) if t in candle_map]
    times = [x[0] for x in sub]
    highs = [x[1]['high'] for x in sub]
    lows = [x[1]['low'] for x in sub]
    closes = [x[1]['close'] for x in sub]
    opens = [x[1]['open'] for x in sub]
    
    n = len(sub)
    # Highest high and lowest low
    h_max = max(highs)
    l_min = min(lows)
    idx_h = highs.index(h_max)
    idx_l = lows.index(l_min)
    
    # Distance in seconds between high and low
    dist_hl_s = abs(idx_h - idx_l) * dt
    # Distance from low to end
    dist_l_end_s = (n - 1 - idx_l) * dt
    # Distance from start to low
    dist_s_l_s = idx_l * dt
    
    print(f"START {s_str} | C={c['C']:3d} | n={n} | L@{idx_l} ({times[idx_l]}) | dist(S->L)={dist_s_l_s}s | dist(L->E)={dist_l_end_s}s | dist(H<->L)={dist_hl_s}s")
