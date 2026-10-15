import json
import pandas as pd
import numpy as np

with open(r'C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\cases_112.json') as f:
    cases = json.load(f)

cases_15s = [c for c in cases if c['dt'] == 15 and c['bars'] >= 50]

rows = []
for c in cases_15s:
    ohlc = c['OHLC']
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    opens = [x['open'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    rng = max(highs) - min(lows)
    sp = (opens[0] - min(lows)) / rng
    ep = (closes[-1] - min(lows)) / rng
    
    # Let's inspect:
    # 1. Total span in seconds
    t_span = (len(ohlc) - 1) * 15
    
    # 2. Last bar direction
    last_body = closes[-1] - opens[-1]
    
    # 3. Pullback from range high at END
    pullback_pts = max(highs) - closes[-1]
    
    # 4. Bars since max high
    i_max = np.argmax(highs)
    bars_since_max = len(ohlc) - 1 - i_max
    
    rows.append({
        'id': c['id'],
        'n': len(ohlc),
        'C': round(c['C']),
        'sp': round(sp, 3),
        'ep': round(ep, 3),
        'pullback': round(pullback_pts, 2),
        'bars_since_max': bars_since_max,
        'last_body': round(last_body, 2)
    })

df = pd.DataFrame(rows)
print(df.to_string())
