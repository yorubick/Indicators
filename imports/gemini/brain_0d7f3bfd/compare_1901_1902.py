import json

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

c77 = next(c for c in data['cases'] if c['START'].startswith('2026-10-12T19:01') and c['bars'] == 21)
c50 = next(c for c in data['cases'] if c['START'].startswith('2026-10-12T19:02') and c['bars'] == 21)

print("Case 19:01 -> 19:21 (C=77):")
print(f"First bar (19:01): {c77['OHLC'][0]}")
print(f"Last bar  (19:21): {c77['OHLC'][-1]}")
print(f"High: {max(x['high'] for x in c77['OHLC'])}, Low: {min(x['low'] for x in c77['OHLC'])}")

print("\nCase 19:02 -> 19:22 (C=50):")
print(f"First bar (19:02): {c50['OHLC'][0]}")
print(f"Last bar  (19:22): {c50['OHLC'][-1]}")
print(f"High: {max(x['high'] for x in c50['OHLC'])}, Low: {min(x['low'] for x in c50['OHLC'])}")

# The candle that left was 19:01
# The candle that entered was 19:22
print("\nCandle 19:01 (left):", c77['OHLC'][0])
print("Candle 19:22 (entered):", c50['OHLC'][-1])
