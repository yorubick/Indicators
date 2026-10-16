import json
import pandas as pd

d12 = json.load(open('data/ohlcv_2m_1430_1516.json'))
df12 = pd.DataFrame(d12)

d14 = json.load(open('data/ohlcv_2m_14oct_1400_1450.json'))
df14 = pd.DataFrame(d14)

print('--- 12-Oct Prices (C = 190 at idx 23) ---')
for i, r in df12.iterrows():
    t = r['time'][11:16]
    print(f"{i:2d} {t} O:{r['open']:8.2f} H:{r['high']:8.2f} L:{r['low']:8.2f} C:{r['close']:8.2f} V:{r['volume']:5d}")

print('\n--- 14-Oct Prices (C = 191 at idx 25) ---')
for i, r in df14.iterrows():
    t = r['time'][11:16]
    print(f"{i:2d} {t} O:{r['open']:8.2f} H:{r['high']:8.2f} L:{r['low']:8.2f} C:{r['close']:8.2f} V:{r['volume']:5d}")
