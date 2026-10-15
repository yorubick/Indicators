import csv, datetime, math
from pathlib import Path
import numpy as np

# Load datasets
ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

ref_1m_path = Path('G:/trading/guias/analisis/manual/Lite_0445_051500_1m_a.csv')
rows_1m = list(csv.DictReader(ref_1m_path.open(encoding='utf-8-sig')))
candles_1m = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_1m}

def ts(d_str, t_str):
    return int(datetime.datetime.fromisoformat(f"{d_str}T{t_str}+00:00").timestamp())

cases = [
    # 15s START sweep (END 19:20:00)
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
    
    # 15s END sweep (START 18:55:00)
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
    
    # 1m Morning (START 04:45:00)
    ('2026-10-12', '04:45:00', '04:50:00', 60, 60, candles_1m),
    ('2026-10-12', '04:45:00', '05:00:00', 60, 60, candles_1m),
    ('2026-10-12', '04:45:00', '05:05:00', 60, 75, candles_1m),
    ('2026-10-12', '04:45:00', '05:15:00', 60, 116, candles_1m),
    ('2026-10-12', '04:45:00', '05:25:00', 60, 113, candles_1m),
    ('2026-10-12', '04:45:00', '05:30:00', 60, 110, candles_1m),
    
    # 1m Evening (END 19:20:00)
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

# Compute variance reduction for single feature splits
features = {}
feature_names = [
    'dt', 'n_bars', 'dur_sec', 'rng', 'rng_ticks',
    'b0_rng', 'b0_body', 'b0_dir', 'b0_high', 'b0_low', 'b0_close',
    'bN_rng', 'bN_body', 'bN_dir', 'bN_high', 'bN_low', 'bN_close',
    'idx_max', 'idx_min', 'bars_from_max', 'bars_from_min',
    'net_chg', 'atr', 'path_len', 'efficiency', 'std_c', 'slope'
]

X_rows = []
Y_vals = []

for d, s, e, dt, C, c_map in cases:
    t_s = ts(d, s)
    t_e = ts(d, e)
    sub = [c_map[t] for t in range(t_s, t_e + dt, dt) if t in c_map]
    if len(sub) < 2:
        continue
    highs = np.array([x['high'] for x in sub])
    lows = np.array([x['low'] for x in sub])
    closes = np.array([x['close'] for x in sub])
    opens = np.array([x['open'] for x in sub])
    
    n = len(sub)
    dur_sec = n * dt
    rng = highs.max() - lows.min()
    rng_ticks = rng / 0.25
    
    b0_rng = highs[0] - lows[0]
    b0_body = abs(closes[0] - opens[0])
    b0_dir = 1.0 if closes[0] >= opens[0] else -1.0
    
    bN_rng = highs[-1] - lows[-1]
    bN_body = abs(closes[-1] - opens[-1])
    bN_dir = 1.0 if closes[-1] >= opens[-1] else -1.0
    
    idx_max = int(np.argmax(highs))
    idx_min = int(np.argmin(lows))
    net_chg = closes[-1] - closes[0]
    tr = np.maximum(highs[1:] - lows[1:], np.maximum(np.abs(highs[1:] - closes[:-1]), np.abs(lows[1:] - closes[:-1])))
    atr = tr.mean() if len(tr) > 0 else (highs[0] - lows[0])
    path_len = np.sum(np.abs(np.diff(closes)))
    efficiency = abs(net_chg) / path_len if path_len > 0 else 1.0
    std_c = np.std(closes)
    slope = np.polyfit(np.arange(n), closes, 1)[0]
    
    row = [
        dt, n, dur_sec, rng, rng_ticks,
        b0_rng, b0_body, b0_dir, highs[0], lows[0], closes[0],
        bN_rng, bN_body, bN_dir, highs[-1], lows[-1], closes[-1],
        idx_max, idx_min, n - 1 - idx_max, n - 1 - idx_min,
        net_chg, atr, path_len, efficiency, std_c, slope
    ]
    X_rows.append(row)
    Y_vals.append(C)

X = np.array(X_rows)
Y = np.array(Y_vals)
total_var = np.var(Y)

print(f"Total cases: {len(Y)}, Mean C: {np.mean(Y):.2f}, Total Var: {total_var:.2f}")

# Find best single split for each feature
best_splits = []
for j, name in enumerate(feature_names):
    col = X[:, j]
    vals = np.unique(col)
    best_gain = 0.0
    best_thresh = None
    for v in vals:
        mask = col <= v
        if mask.sum() < 3 or (~mask).sum() < 3:
            continue
        v_left = np.var(Y[mask]) * mask.sum()
        v_right = np.var(Y[~mask]) * (~mask).sum()
        gain = total_var * len(Y) - (v_left + v_right)
        if gain > best_gain:
            best_gain = gain
            best_thresh = v
    if best_thresh is not None:
        best_splits.append((name, best_gain / (total_var * len(Y)), best_thresh))

best_splits.sort(key=lambda x: -x[1])
print("\nTop features by variance reduction on C:")
for name, frac, thresh in best_splits[:12]:
    print(f"  {name:<16}: explains {frac*100:5.1f}% var at threshold <= {thresh}")
