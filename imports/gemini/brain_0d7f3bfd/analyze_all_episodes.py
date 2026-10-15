import json
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

cases = data['cases']

rows = []
for c in cases:
    cid = c['id']
    parts = cid.split('_')
    t_start = parts[1]
    t_end = parts[2]
    dt = c['dt']
    bars = c['bars']
    act_c = c['C']
    split = c['split']
    branch = c['branch']
    
    # get ohlc range
    ohlc = c.get('OHLC', [])
    if ohlc:
        highs = [x['high'] for x in ohlc]
        lows = [x['low'] for x in ohlc]
        opens = [x['open'] for x in ohlc]
        closes = [x['close'] for x in ohlc]
        rng = max(highs) - min(lows)
        sp = (opens[0] - min(lows)) / rng if rng > 0 else 0.5
    else:
        rng = 0
        sp = 0
        
    rows.append({
        'id': cid,
        'start': t_start,
        'end': t_end,
        'bars': bars,
        'dt': dt,
        'C': act_c,
        'rng': rng,
        'start_pos': sp,
        'split': split,
        'branch': branch
    })

df = pd.DataFrame(rows)
df_long = df[df['bars'] >= 21]

print("=== ALL LONG CASES IN DATASET (bars >= 21) ===")
print(df_long[['id', 'start', 'end', 'bars', 'C', 'rng', 'start_pos', 'split']].to_string())
