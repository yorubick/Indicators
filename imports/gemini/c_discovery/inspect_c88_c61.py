import json
import pandas as pd

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = {c['id']: c for c in master['cases']}

c88 = cases['20261012_190315_192345_15s']
c61 = cases['20261012_190330_192345_15s']

df88 = pd.DataFrame(c88['OHLCV'])
df61 = pd.DataFrame(c61['OHLCV'])

print(f"C88 bars: {len(df88)}, C61 bars: {len(df61)}")
print("\nFirst 5 bars of C88:")
print(df88.iloc[:5])

print("\nFirst 5 bars of C61:")
print(df61.iloc[:5])

print("\nThe dropped candle (present in C88, absent in C61):")
print(df88.iloc[0])

print("\nGlobal High and Low:")
print("C88: High =", df88['high'].max(), "at idx", df88['high'].idxmax(), "time", df88.iloc[df88['high'].idxmax()]['time'])
print("C88: Low  =", df88['low'].min(), "at idx", df88['low'].idxmin(), "time", df88.iloc[df88['low'].idxmin()]['time'])

print("C61: High =", df61['high'].max(), "at idx", df61['high'].idxmax(), "time", df61.iloc[df61['high'].idxmax()]['time'])
print("C61: Low  =", df61['low'].min(), "at idx", df61['low'].idxmin(), "time", df61.iloc[df61['low'].idxmin()]['time'])
