import json
import pandas as pd

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = {c['id']: c for c in master['cases']}

target_ids = [
    '20261012_185800_191800_60s',
    '20261012_185900_191900_60s',
    '20261012_190000_192000_60s',
    '20261012_190100_192100_60s',
    '20261012_190200_192200_60s',
    '20261012_190300_192300_60s',
    '20261012_190400_192400_60s',
]

for tid in target_ids:
    if tid in cases:
        c = cases[tid]
        df = pd.DataFrame(c['OHLCV'])
        print("="*60)
        print(f"ID: {tid} | C: {c['C_Lite']} | bars: {len(df)}")
        print(f"Start bar time: {df.iloc[0]['time']} ({c['START']})")
        print(f"End bar time:   {df.iloc[-1]['time']} ({c['END']})")
        print(f"High: {df['high'].max()} at index {df['high'].idxmax()} (time {df.iloc[df['high'].idxmax()]['time']})")
        print(f"Low:  {df['low'].min()} at index {df['low'].idxmin()} (time {df.iloc[df['low'].idxmin()]['time']})")
        print("First 3 bars:")
        print(df.iloc[:3][['time', 'open', 'high', 'low', 'close', 'volume']])
        print("Last 3 bars:")
        print(df.iloc[-3:][['time', 'open', 'high', 'low', 'close', 'volume']])
