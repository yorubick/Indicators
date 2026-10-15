import json

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

# Let's find cases starting around 18:55 to 19:00 and ending at 19:20
for c in data['cases']:
    if '192000' in c['id'] and c['dt'] == 60:
        print(f"ID: {c['id']}, bars={c['bars']}, C={c['C']}")
        ohlc = c['OHLC']
        highs = [x['high'] for x in ohlc]
        lows = [x['low'] for x in ohlc]
        print(f"   rng={max(highs)-min(lows)}, high={max(highs)}, low={min(lows)}")
