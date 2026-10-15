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

cases = [
    # 15s cases
    ('2026-10-12', '18:54:00', '19:20:00', 15, 123, candles_15s),
    ('2026-10-12', '18:54:15', '19:20:00', 15, 118, candles_15s),
    ('2026-10-12', '18:54:30', '19:20:00', 15, 67, candles_15s),
    ('2026-10-12', '18:54:45', '19:20:00', 15, 67, candles_15s),
    ('2026-10-12', '18:55:00', '19:20:00', 15, 106, candles_15s),
    ('2026-10-12', '18:55:15', '19:20:00', 15, 66, candles_15s),
    ('2026-10-12', '18:55:30', '19:20:00', 15, 88, candles_15s),
    ('2026-10-12', '18:55:45', '19:20:00', 15, 88, candles_15s),
    ('2026-10-12', '18:56:00', '19:20:00', 15, 106, candles_15s),
    ('2026-10-12', '18:56:15', '19:20:00', 15, 67, candles_15s),
    ('2026-10-12', '18:56:30', '19:20:00', 15, 67, candles_15s),
    ('2026-10-12', '18:56:45', '19:20:00', 15, 79, candles_15s),
    ('2026-10-12', '18:57:00', '19:20:00', 15, 67, candles_15s),
    ('2026-10-12', '18:55:00', '19:18:00', 15, 88, candles_15s),
    ('2026-10-12', '18:55:00', '19:19:00', 15, 115, candles_15s),
    ('2026-10-12', '18:55:00', '19:20:15', 15, 79, candles_15s),
    ('2026-10-12', '18:55:00', '19:20:30', 15, 67, candles_15s),
    ('2026-10-12', '18:55:00', '19:20:45', 15, 66, candles_15s),
    ('2026-10-12', '18:55:00', '19:21:00', 15, 115, candles_15s),
    ('2026-10-12', '18:55:00', '19:21:15', 15, 106, candles_15s),
    ('2026-10-12', '18:55:00', '19:21:30', 15, 79, candles_15s),
    ('2026-10-12', '18:55:00', '19:21:45', 15, 66, candles_15s),
    ('2026-10-12', '18:55:00', '19:22:00', 15, 106, candles_15s),
    
    # 1m cases
    ('2026-10-12', '04:45:00', '04:50:00', 60, 60, candles_1m),
    ('2026-10-12', '04:45:00', '05:00:00', 60, 60, candles_1m),
    ('2026-10-12', '04:45:00', '05:05:00', 60, 75, candles_1m),
    ('2026-10-12', '04:45:00', '05:15:00', 60, 116, candles_1m),
    ('2026-10-12', '04:45:00', '05:25:00', 60, 113, candles_1m),
    ('2026-10-12', '04:45:00', '05:30:00', 60, 110, candles_1m),
    ('2026-10-12', '18:50:00', '19:20:00', 60, 118, candles_1m),
    ('2026-10-12', '18:54:00', '19:20:00', 60, 134, candles_1m),
    ('2026-10-12', '18:55:00', '19:20:00', 60, 62, candles_1m),
    ('2026-10-12', '18:56:00', '19:20:00', 60, 109, candles_1m),
    ('2026-10-12', '18:57:00', '19:20:00', 60, 77, candles_1m),
    ('2026-10-12', '18:58:00', '19:20:00', 60, 77, candles_1m),
    ('2026-10-12', '18:59:00', '19:20:00', 60, 77, candles_1m),
    ('2026-10-12', '19:00:00', '19:20:00', 60, 77, candles_1m),
    ('2026-10-12', '19:11:00', '19:31:00', 60, 80, candles_1m),
]

print(f"Loaded {len(cases)} cases.")

# Compute features for each case
data = []
for d, s, e, dt, C, c_map in cases:
    t_s = ts(d, s)
    t_e = ts(d, e)
    sub = [c_map[t] for t in range(t_s, t_e + dt, dt) if t in c_map]
    if len(sub) < 2:
        continue
    highs = [x['high'] for x in sub]
    lows = [x['low'] for x in sub]
    closes = [x['close'] for x in sub]
    opens = [x['open'] for x in sub]
    
    # Range
    h = max(highs)
    l = min(lows)
    rng = h - l
    n_bars = len(sub)
    
    # Bar index of highest and lowest
    ih = highs.index(h)
    il = lows.index(l)
    
    # Distance from max/min to end
    bars_from_max_to_end = n_bars - 1 - ih
    bars_from_min_to_end = n_bars - 1 - il
    
    # True range
    tr = [highs[0] - lows[0]] + [max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1])) for i in range(1, n_bars)]
    atr = sum(tr) / n_bars
    
    # Standard deviation of closes
    std_c = float(np.std(closes))
    
    # Linear regression slope of closes
    x_axis = np.arange(n_bars)
    slope, intercept = np.polyfit(x_axis, closes, 1)
    
    data.append({
        'name': f"{s}-{e} ({dt}s)",
        'dt': dt, 'C': C, 'n_bars': n_bars,
        'h': h, 'l': l, 'rng': rng,
        'ih': ih, 'il': il,
        'bars_from_max': bars_from_max_to_end,
        'bars_from_min': bars_from_min_to_end,
        'atr': atr, 'std_c': std_c,
        'slope': slope,
        'start_c': closes[0], 'end_c': closes[-1],
        'net_change': closes[-1] - closes[0]
    })

print(f"Processed {len(data)} valid cases.")

# Let's inspect some cases
print(f"{'Case':<22} | dt | {'C':>4} | bars | {'Rng':>6} | {'ATR':>5} | b_max | b_min | {'Slope':>6}")
print("-" * 75)
for d in data[:25]:
    print(f"{d['name']:<22} | {d['dt']:2d} | {d['C']:4d} | {d['n_bars']:4d} | {d['rng']:6.2f} | {d['atr']:5.2f} | {d['bars_from_max']:5d} | {d['bars_from_min']:5d} | {d['slope']:6.3f}")

