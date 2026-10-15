import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

cases = data['cases']
long_cases = [c for c in cases if c['bars'] >= 21]

print(f"Total long cases: {len(long_cases)}")

results = []
for c in long_cases:
    ohlc = c['OHLC']
    n = c['bars']
    dt = c['dt']
    C = round(c['C'])
    split = c['split']
    
    highs = np.array([x['high'] for x in ohlc])
    lows = np.array([x['low'] for x in ohlc])
    closes = np.array([x['close'] for x in ohlc])
    opens = np.array([x['open'] for x in ohlc])
    
    rng = np.max(highs) - np.min(lows)
    ticks = rng / 0.25 # NQ ticks
    
    imax = int(np.argmax(highs))
    imin = int(np.argmin(lows))
    
    # Distance between global extremes
    dist_extrema_bars = abs(imax - imin)
    dist_extrema_sec = dist_extrema_bars * dt
    
    # Distance from extreme to END
    bars_from_high_to_end = n - 1 - imax
    bars_from_low_to_end = n - 1 - imin
    
    # Distance from START to first extreme
    first_ext_bar = min(imax, imin)
    bars_start_to_ext = first_ext_bar
    
    # True ranges
    trs = [highs[0] - lows[0]]
    for i in range(1, n):
        trs.append(max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1])))
    atr = np.mean(trs)
    sum_tr = np.sum(trs)
    
    # Efficiency / path
    path = np.sum(np.abs(np.diff(closes)))
    net = abs(closes[-1] - opens[0])
    er = net / path if path > 0 else 0
    
    # Timespan
    t_span = (n - 1) * dt
    t_tot = n * dt
    
    # Short rule projection:
    c_short = n * dt * 10 / 183
    
    results.append({
        'id': c['id'],
        'split': split,
        'START': c['START'][11:16],
        'END': c['END'][11:16],
        'n': n,
        'dt': dt,
        'C': C,
        'lambda': C / dt,
        'rng': rng,
        'ticks': ticks,
        'atr': atr,
        'sum_tr': sum_tr,
        'dist_ext_bars': dist_extrema_bars,
        'bars_from_high': bars_from_high_to_end,
        'bars_from_low': bars_from_low_to_end,
        'c_short': c_short,
        't_span': t_span,
        'ratio_tspan_C': t_span / C,
        'ratio_ticks_C': ticks / C,
        'ratio_sumtr_C': sum_tr / C,
        'er': er,
    })

df = pd.DataFrame(results)
print("Computed features for all 59 cases.")
