import json

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

for c in data['cases']:
    if c['id'] in ['20261012_185800_191800_60s', '20261012_185900_191900_60s', '20261012_190000_192000_60s']:
        print(f"ID: {c['id']}, bars={c['bars']}, C={c['C']}")
        ohlc = c['OHLC']
        highs = [x['high'] for x in ohlc]
        lows = [x['low'] for x in ohlc]
        opens = [x['open'] for x in ohlc]
        closes = [x['close'] for x in ohlc]
        rng = max(highs) - min(lows)
        sp = (opens[0] - min(lows)) / rng
        print(f"   rng={rng}, start_pos={sp:.2f}, open[0]={opens[0]}, high={max(highs)}, low={min(lows)}")
        print(f"   arg_max={highs.index(max(highs))}, arg_min={lows.index(min(lows))}")
