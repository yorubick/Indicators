import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

with open(r'G:\trading\guias\analisis\C_evolucion87_resultados.json') as f:
    data13 = json.load(f)

# Collect all baseline / plateau episodes (for n=21..23 where no extreme breakout is happening)
episodes = [
    {'name': '14:00 (12 Oct)', 'start': '14:00', 'end': '14:20', 'C': 62, 'dt': 60, 'n': 21},
    {'name': '15:30 (12 Oct)', 'start': '15:30', 'end': '15:50', 'C': 69, 'dt': 60, 'n': 21},
    {'name': '15:31 (12 Oct)', 'start': '15:31', 'end': '15:51', 'C': 68, 'dt': 60, 'n': 21},
    {'name': '07:00 (12 Oct)', 'start': '07:00', 'end': '07:20', 'C': 75, 'dt': 60, 'n': 21},
    {'name': '04:45 (12 Oct)', 'start': '04:45', 'end': '05:05', 'C': 75, 'dt': 60, 'n': 21},
    {'name': '06:00 (12 Oct)', 'start': '06:00', 'end': '06:20', 'C': 77, 'dt': 60, 'n': 21},
    {'name': '19:00 (12 Oct)', 'start': '19:00', 'end': '19:20', 'C': 77, 'dt': 60, 'n': 21},
    {'name': '19:01 (12 Oct)', 'start': '19:01', 'end': '19:21', 'C': 77, 'dt': 60, 'n': 21},
    {'name': '19:00 (13 Oct)', 'start': '19:00', 'end': '19:20', 'C': 81, 'dt': 60, 'n': 21},
    {'name': '06:25 (13 Oct)', 'start': '06:25', 'end': '06:46', 'C': 84, 'dt': 60, 'n': 22},
    {'name': '19:02 (12 Oct, comp)', 'start': '19:02', 'end': '19:22', 'C': 50, 'dt': 60, 'n': 21},
]

# Extract actual metrics for each from verified dataset or 13 Oct dataset
rows = []
for ep in episodes:
    # find in data['cases']
    match = None
    for c in data['cases']:
        if c['START'].startswith(f"2026-10-12T{ep['start']}") and c['bars'] == ep['n'] and c['dt'] == ep['dt']:
            match = c
            break
        elif c['START'].startswith(f"2026-10-13T{ep['start']}") and c['bars'] == ep['n'] and c['dt'] == ep['dt']:
            match = c
            break
            
    if match is not None:
        ohlc = match['OHLC']
        highs = [x['high'] for x in ohlc]
        lows = [x['low'] for x in ohlc]
        closes = [x['close'] for x in ohlc]
        rng = max(highs) - min(lows)
        trs = [highs[0]-lows[0]] + [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, len(closes))]
        atr = np.mean(trs)
    elif ep['name'] == '06:25 (13 Oct)':
        # from data13
        case_data = next(x for x in data13['cases'] if x['bars'] == 22)
        rng = case_data['range_high'] - case_data['range_low']
        atr = 8.0 # approximate
    else:
        continue
        
    rows.append({
        'name': ep['name'],
        'C': ep['C'],
        'n': ep['n'],
        'range': rng,
        'atr': atr,
        'ratio_rng_atr': rng / atr,
        'ticks': rng / 0.25,
        'c_over_dt': ep['C'] / ep['dt'],
        'c_times_rng': ep['C'] * rng,
        'c_div_rng': ep['C'] / rng if rng > 0 else 0
    })

df = pd.DataFrame(rows).sort_values('C')
print(df.to_string())
