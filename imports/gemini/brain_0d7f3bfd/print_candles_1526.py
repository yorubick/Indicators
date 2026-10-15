import json
from datetime import datetime, timezone

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

# Find case 15:26 -> 15:51
c = next(x for x in data['cases'] if x['START'].startswith('2026-10-12T15:26') and x['bars'] == 26)

print("Time     | Open     | High     | Low      | Close    | Range | Dir")
print("-" * 65)
for b in c['OHLC']:
    dt_str = datetime.fromtimestamp(b['time'], timezone.utc).strftime('%H:%M:%S')
    rng = b['high'] - b['low']
    d = "UP" if b['close'] >= b['open'] else "DN"
    print(f"{dt_str} | {b['open']:8.2f} | {b['high']:8.2f} | {b['low']:8.2f} | {b['close']:8.2f} | {rng:5.2f} | {d}")
