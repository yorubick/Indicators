import json
import numpy as np
import pandas as pd

with open(r'C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\cases_112.json') as f:
    cases = json.load(f)

add_cases = cases[99:]
rows = []
for c in add_cases:
    ohlc = c['OHLC']
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    opens = [x['open'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    rng = max(highs) - min(lows)
    sp = (opens[0] - min(lows)) / rng if rng > 0 else 0.5
    ep = (closes[-1] - min(lows)) / rng if rng > 0 else 0.5
    trs = [highs[0]-lows[0]] + [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, len(closes))]
    atr = np.mean(trs)
    dt = c['dt']
    bars = c['bars']
    t_span = (bars - 1) * dt
    
    rows.append({
        'id': c['id'],
        'dt': dt,
        'bars': bars,
        't_span_s': t_span,
        'act_C': round(c['C'], 2),
        'rng': round(rng, 2),
        'atr': round(atr, 2),
        'sp': round(sp, 2),
        'ep': round(ep, 2),
        'dir': 'BULL' if closes[-1] > opens[0] else 'BEAR',
        'C_over_tspan': round(c['C'] / t_span, 4),
        'tspan_over_C': round(t_span / c['C'], 2)
    })

df = pd.DataFrame(rows)
print("=== 13 ADDITIONAL CONTROLS DETAILED FEATURES ===")
print(df.to_string())
