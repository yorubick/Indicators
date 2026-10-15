import json

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

print("Cases with C in [50, 52, 55, 60] with n >= 21:")
for c in data['cases']:
    if c['bars'] >= 21 and round(c['C']) in [50, 52, 55, 60]:
        ohlc = c['OHLC']
        highs = [x['high'] for x in ohlc]
        lows = [x['low'] for x in ohlc]
        print(f"ID: {c['id']}, bars={c['bars']}, C={c['C']}, rng={max(highs)-min(lows)}, high={max(highs)}, low={min(lows)}")
