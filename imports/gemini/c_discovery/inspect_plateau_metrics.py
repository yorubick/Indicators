import json
import pandas as pd

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = {c['id']: c for c in master['cases']}

test_ids = [
    '20261012_060000_062000_60s', # C=77
    '20261012_185800_191800_60s', # C=77
    '20261012_185900_191900_60s', # C=77
    '20261012_190000_192000_60s', # C=77
    '20261012_190100_192100_60s', # C=77
    '20261012_190200_192200_60s', # C=50
    '20261012_190300_192300_60s', # C=50
    '20261012_190400_192400_60s', # C=50
    '20261012_140000_142000_60s', # C=62
    '20261012_185500_192000_60s', # C=62
    '20261012_185400_192000_60s', # C=134
]

rows = []
for tid in test_ids:
    c = cases[tid]
    df = pd.DataFrame(c['OHLCV'])
    r_high = df['high'].max()
    r_low = df['low'].min()
    rng = r_high - r_low
    rng_ticks = rng * 4.0
    start_open = df.iloc[0]['open']
    end_close = df.iloc[-1]['close']
    net_pts = end_close - start_open
    net_ticks = net_pts * 4.0
    vol_sum = df['volume'].sum()
    
    rows.append({
        'id': tid,
        'C': c['C_Lite'],
        'rng_pts': rng,
        'rng_ticks': rng_ticks,
        'net_pts': net_pts,
        'net_ticks': net_ticks,
        'vol': vol_sum,
        'vol_mean': round(vol_sum / len(df), 1),
    })

res = pd.DataFrame(rows)
print(res.to_string(index=False))
