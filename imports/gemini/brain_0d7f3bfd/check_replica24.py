import json
import numpy as np

with open(r'C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\cases_112.json') as f:
    cases = json.load(f)

for c in cases:
    if c['id'] in ['replica24_1', 'replica24_2']:
        ohlc = c['OHLC']
        highs = [x['high'] for x in ohlc]
        lows = [x['low'] for x in ohlc]
        opens = [x['open'] for x in ohlc]
        closes = [x['close'] for x in ohlc]
        rng = max(highs) - min(lows)
        sp = (opens[0] - min(lows)) / rng
        ep = (closes[-1] - min(lows)) / rng
        trs = [highs[0]-lows[0]] + [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, len(closes))]
        atr = np.mean(trs)
        print(f"ID: {c['id']} | C={c['C']} | rng={rng:.2f} | atr={atr:.2f} | rng/atr={rng/atr:.2f} | sp={sp:.2f} | ep={ep:.2f}")
        print(f"   open0={opens[0]}, high={max(highs)}, low={min(lows)}, close_end={closes[-1]}")
