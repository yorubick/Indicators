import json
from datetime import datetime, timezone

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

c = next(x for x in data['cases'] if x['START'].startswith('2026-10-12T14:00') and x['bars'] == 24)

print("Time     | Open     | High     | Low      | Close    | Range | Dir")
print("-" * 65)
for b in c['OHLC'][-6:]:
    dt_str = datetime.fromtimestamp(b['time'], timezone.utc).strftime('%H:%M:%S')
    rng = b['high'] - b['low']
    d = "UP" if b['close'] >= b['open'] else "DN"
    print(f"{dt_str} | {b['open']:8.2f} | {b['high']:8.2f} | {b['low']:8.2f} | {b['close']:8.2f} | {rng:5.2f} | {d}")
