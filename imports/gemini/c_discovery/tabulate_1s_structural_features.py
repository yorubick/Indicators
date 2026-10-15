import json
import glob
import os
import pandas as pd
import numpy as np

# Load all 1s results
data_files = [
    r'G:\trading\guias\analisis\C_1s_salida_meseta_resultados.json',
    r'G:\trading\guias\analisis\C_1s_cruce_START_resultados.json',
    r'G:\trading\guias\analisis\C_1s_1402_n27_n28_resultados.json',
    r'G:\trading\guias\analisis\C_frontera_1s_replicas_resultados.json',
]

all_cases = []

# 1. salida meseta
with open(data_files[0], 'r', encoding='utf-8') as f:
    d = json.load(f)
for r in d['results']:
    all_cases.append({
        'dataset': 'salida_meseta',
        'id': f"140400_n{r['bars']}",
        'start_utc': r['START_UTC'],
        'end_utc': r['END_UTC'],
        'n': r['bars'],
        'C': r['C'],
        'C_int': round(r['C']),
        'ohlc': r['OHLC'],
        'high': r['high'],
        'low': r['low'],
        'last_bar': r['END_OHLCV']
    })

# 2. cruce start
with open(data_files[1], 'r', encoding='utf-8') as f:
    d = json.load(f)
for r in d['results']:
    all_cases.append({
        'dataset': 'cruce_start',
        'id': f"140401_n{r['bars']}",
        'start_utc': r['START_UTC'],
        'end_utc': r['END_UTC'],
        'n': r['bars'],
        'C': r['C'],
        'C_int': round(r['C']),
        'ohlc': r['OHLC'],
        'high': r['high'],
        'low': r['low'],
        'last_bar': r['OHLC'][-1]
    })

# 3. 1402 n27 n28
with open(data_files[2], 'r', encoding='utf-8') as f:
    d = json.load(f)
for r in d['results']:
    all_cases.append({
        'dataset': '1402_n27_n28',
        'id': f"140200_n{r['bars']}",
        'start_utc': d['spec']['START_UTC'],
        'end_utc': r['END_UTC'],
        'n': r['bars'],
        'C': r['C'],
        'C_int': round(r['C']),
        'ohlc': r['OHLC'],
        'high': r['high'],
        'low': r['low'],
        'last_bar': r['OHLC'][-1]
    })

# 4. frontera 1s replicas
if os.path.exists(data_files[3]):
    with open(data_files[3], 'r', encoding='utf-8') as f:
        d = json.load(f)
    for r in d.get('results', []):
        all_cases.append({
            'dataset': 'frontera_replicas',
            'id': f"{r.get('id', 'rep')}",
            'start_utc': r.get('START_UTC'),
            'end_utc': r.get('END_UTC'),
            'n': r.get('bars'),
            'C': r.get('C'),
            'C_int': round(r['C']),
            'ohlc': r.get('OHLC'),
            'high': r.get('high'),
            'low': r.get('low'),
            'last_bar': r.get('OHLC', [{}])[-1]
        })

print(f"Total 1s cases loaded: {len(all_cases)}")

rows = []
for c in all_cases:
    ohlc = c['ohlc']
    n = c['n']
    high = c['high']
    low = c['low']
    rng = high - low
    last = c['last_bar']
    close = last['close']
    c_int = c['C_int']
    
    # Metrics
    # 1. relative position in range [0 = at low, 1 = at high]
    pos_in_range = (close - low) / rng if rng > 0 else 0.5
    # 2. distance to nearest extreme [0 = at extreme, 0.5 = at exact midpoint]
    dist_extreme = min(pos_in_range, 1.0 - pos_in_range)
    # 3. ratio of n to 18.3
    n_over_183 = n / 18.3
    # 4. net excursion from first bar open
    open_0 = ohlc[0]['open']
    net_excursion = (close - open_0) / rng if rng > 0 else 0
    # 5. bar of high and bar of low (relative index)
    idx_high = max(range(len(ohlc)), key=lambda i: ohlc[i]['high'])
    idx_low = min(range(len(ohlc)), key=lambda i: ohlc[i]['low'])
    # 6. bars since high, bars since low
    bars_since_high = (n - 1) - idx_high
    bars_since_low = (n - 1) - idx_low
    
    rows.append({
        'id': c['id'],
        'n': n,
        'C': c['C'],
        'C_int': c_int,
        'high': high,
        'low': low,
        'range': rng,
        'close': close,
        'pos_range': pos_in_range,
        'dist_ext': dist_extreme,
        'n/18.3': n_over_183,
        'net_exc': net_excursion,
        'bs_high': bars_since_high,
        'bs_low': bars_since_low
    })

df = pd.DataFrame(rows)
df = df.sort_values(by=['id', 'n'])
print(df[['id', 'n', 'C_int', 'high', 'low', 'range', 'close', 'pos_range', 'dist_ext', 'n/18.3', 'bs_high', 'bs_low']].to_string(index=False))
