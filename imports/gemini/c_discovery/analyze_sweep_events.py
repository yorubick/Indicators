import json
import pandas as pd
import numpy as np

with open(r"G:\trading\guias\analisis\C_barrido_END_1855_1920_1924_15s.json", "r", encoding="utf-8") as f:
    barrido = json.load(f)

cases = barrido["cases"]

# The full 17 candles of the sweep:
# Let's get the OHLCV of the last case (which contains all 17 candles)
last_case_ohlcv = pd.DataFrame(cases[-1]["OHLCV"])
# The sweep starts at 19:20:00 (which is 16 bars before the end)
sweep_bars = last_case_ohlcv.iloc[-17:].copy().reset_index(drop=True)
sweep_bars['C'] = [c['C_Lite'] for c in cases]
sweep_bars['time_str'] = [c['END'].split('T')[1][:8] for c in cases]

sweep_bars['hl2'] = (sweep_bars['high'] + sweep_bars['low']) / 2.0
sweep_bars['hlc3'] = (sweep_bars['high'] + sweep_bars['low'] + sweep_bars['close']) / 3.0
sweep_bars['range'] = sweep_bars['high'] - sweep_bars['low']
sweep_bars['body'] = sweep_bars['close'] - sweep_bars['open']

# Global high and low at each step:
g_highs = []
g_lows = []
dist_g_high = []
dist_g_low = []
for i, c in enumerate(cases):
    df_i = pd.DataFrame(c['OHLCV'])
    gh = df_i['high'].max()
    gl = df_i['low'].min()
    g_highs.append(gh)
    g_lows.append(gl)
    dist_g_high.append(gh - df_i.iloc[-1]['close'])
    dist_g_low.append(df_i.iloc[-1]['close'] - gl)

sweep_bars['g_high'] = g_highs
sweep_bars['g_low'] = g_lows
sweep_bars['dist_gh'] = dist_g_high
sweep_bars['dist_gl'] = dist_g_low

print(sweep_bars[['time_str', 'C', 'open', 'high', 'low', 'close', 'range', 'body', 'volume', 'dist_gh']].to_string())
