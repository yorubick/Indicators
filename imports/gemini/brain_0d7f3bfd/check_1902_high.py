import json

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

# Find 1902 to 1922
for c in data['cases']:
    if c['id'] == '20261012_190200_192200_60s':
        ohlc = c['OHLC']
        highs = [x['high'] for x in ohlc]
        print("1902 to 1922 highs:")
        print(highs)
        print("Max of all highs:", max(highs))
        print("High[-1]:", highs[-1])
        print("Max of highs[:-1]:", max(highs[:-1]))
        print("is_new_high:", highs[-1] > max(highs[:-1]))
        print("is_equal_high:", highs[-1] == max(highs[:-1]))
