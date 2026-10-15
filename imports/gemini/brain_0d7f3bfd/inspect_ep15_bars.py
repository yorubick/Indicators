import json
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

# Find the longest case in Episode 15, which is 15:26 to 15:51 (26 bars)
# Let's see all candles in this case
for c in data['cases']:
    if c['id'] == '20261012_152600_155100_60s':
        ohlc = c['OHLC']
        print(f"Case {c['id']}, bars={len(ohlc)}")
        for i, bar in enumerate(ohlc):
            t = 1526 + i
            # Format time
            mm = (26 + i) % 60
            hh = 15 + (26 + i) // 60
            t_str = f"{hh:02d}:{mm:02d}"
            print(f"Bar {i:2d} ({t_str}): O={bar['open']:.2f}, H={bar['high']:.2f}, L={bar['low']:.2f}, C={bar['close']:.2f}")
        break
