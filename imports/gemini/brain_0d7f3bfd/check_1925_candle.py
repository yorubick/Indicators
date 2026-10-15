import json

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

for c in data['cases']:
    if c['id'] == '20261012_190400_192500_60s':
        ohlc = c['OHLC']
        print("Bars in 1904 to 1925:", len(ohlc))
        for i, b in enumerate(ohlc[-5:]):
            idx = len(ohlc) - 5 + i
            # 1904 + idx minutes
            mm = 4 + idx
            print(f"Bar {idx} (19:{mm:02d}): O={b['open']}, H={b['high']}, L={b['low']}, C={b['close']}")
        break
