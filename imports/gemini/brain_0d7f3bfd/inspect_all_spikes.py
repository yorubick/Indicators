import json
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

cases = data['cases']

# Group by episode prefix (date + hour/start)
# Let's inspect the spikes:
# Ep 14 (14:00): base 62 -> 14:22 is 83 (+21), 14:23 is 76 (+14)
# Ep 19 (19:00): base 77 -> 19:21 is 102 (+25), 19:24 is 60 (-17)
# Ep 19 (19:04): base 71 -> 19:28 is 128 (+57), 19:29 is 134 (+63), 19:30 is 109 (+38)
# Ep 15 (15:27): base 68/82 -> 15:51 is 93
# Ep 07 (06:57): base 78 -> 06:57 is 87 (+9)
# Oct 13 (06:45): base 84 -> 06:45 is 87 (+3)

print("Checking deviations from base across all episodes...")
