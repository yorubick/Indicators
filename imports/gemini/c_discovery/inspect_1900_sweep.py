import json
import pandas as pd

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = {c['id']: c for c in master['cases']}

ids = [
    '20261012_190000_192000_60s',
    '20261012_190000_192100_60s',
    '20261012_190000_192200_60s',
    '20261012_190000_192300_60s',
    '20261012_190000_192400_60s',
]

rows = []
for cid in ids:
    c = cases.get(cid)
    if c:
        df = pd.DataFrame(c['OHLCV'])
        last = df.iloc[-1]
        rows.append({
            'id': cid,
            'n': len(df),
            'C': c['C_Lite'],
            'last_time': last['time'],
            'open': last['open'],
            'high': last['high'],
            'low': last['low'],
            'close': last['close'],
            'vol': last['volume'],
            'global_high': df['high'].max(),
            'global_low': df['low'].min(),
            'high_idx': df['high'].idxmax(),
            'low_idx': df['low'].idxmin()
        })
    else:
        print(f"Missing {cid}")

res = pd.DataFrame(rows)
print(res.to_string(index=False))
