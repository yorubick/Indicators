import json
import numpy as np
import pandas as pd

with open(r'C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\cases_112.json') as f:
    cases = json.load(f)

cases_15s = [c for c in cases if c['dt'] == 15 and c['bars'] >= 50]
print(f"Total long 15s cases: {len(cases_15s)}")

table = []
for c in cases_15s:
    ohlc = c['OHLC']
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    opens = [x['open'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    n = len(ohlc)
    
    rng = max(highs) - min(lows)
    sp = (opens[0] - min(lows)) / rng
    ep = (closes[-1] - min(lows)) / rng
    
    # Check end bar features
    # Did last bar make a local pivot or swing?
    end_o = opens[-1]
    end_h = highs[-1]
    end_l = lows[-1]
    end_c = closes[-1]
    
    # Check last 4 bars (last 1 minute)
    last_1m_high = max(highs[-4:])
    last_1m_low = min(lows[-4:])
    last_1m_close = closes[-1]
    
    # Max high bar index and min low bar index
    i_max = np.argmax(highs)
    i_min = np.argmin(lows)
    dist_max = n - 1 - i_max
    dist_min = n - 1 - i_min
    
    table.append({
        'id': c['id'],
        'bars': n,
        'C': round(c['C']),
        'start_pos': round(sp, 3),
        'end_pos': round(ep, 3),
        'dist_max': dist_max,
        'dist_min': dist_min,
        'end_c': end_c,
        'end_h': end_h,
        'end_l': end_l
    })

df = pd.DataFrame(table)
print(df.to_string())
