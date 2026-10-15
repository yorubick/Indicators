import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

spike_ids = [
    '20261012_140000_142200_60s',
    '20261012_140000_142300_60s',
    '20261012_190000_192100_60s',
    '20261012_190400_192800_60s',
    '20261012_190400_192900_60s',
    '20261012_190400_193000_60s',
    '20261012_152700_155100_60s',
    '20261012_152800_155000_60s'
]

print("=== SPIKE CASES DETAILED BREAKDOWN ===")
for cid in spike_ids:
    for c in data['cases']:
        if c['id'] == cid:
            ohlc = c['OHLC']
            n = len(ohlc)
            highs = [x['high'] for x in ohlc]
            lows = [x['low'] for x in ohlc]
            opens = [x['open'] for x in ohlc]
            closes = [x['close'] for x in ohlc]
            rng = max(highs) - min(lows)
            
            # last 3 bars
            last_bars = []
            for j in range(max(0, n-3), n):
                last_bars.append(f"bar{j}: O={opens[j]} H={highs[j]} L={lows[j]} C={closes[j]}")
                
            print(f"ID: {cid}")
            print(f"  Bars: {n}, C: {c['C']}, Range: {rng}")
            print("  Last bars:\n    " + "\n    ".join(last_bars))
            break
