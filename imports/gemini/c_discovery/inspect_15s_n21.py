import json
import pandas as pd

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = {c['id']: c for c in master['cases']}

c15_21 = cases['20261012_190000_190500_15s']
c15_20 = cases.get('20261012_190000_190445_15s')
c15_19 = cases.get('20261012_190000_190430_15s')

df21 = pd.DataFrame(c15_21['OHLCV'])
print(f"15s case at n=21: C={c15_21['C_Lite']}")
print(f"Start: {df21.iloc[0]['time']} ({c15_21['START']})")
print(f"End:   {df21.iloc[-1]['time']} ({c15_21['END']})")
print("Last 3 candles:")
print(df21.iloc[-3:])

# Check all candles
print("\nGlobal High and Low:")
print("High:", df21['high'].max(), "at idx", df21['high'].idxmax())
print("Low: ", df21['low'].min(), "at idx", df21['low'].idxmin())
print("Range:", df21['high'].max() - df21['low'].min())
