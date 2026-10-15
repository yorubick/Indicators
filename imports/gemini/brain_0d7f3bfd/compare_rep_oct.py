import json

with open(r'C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\cases_112.json') as f:
    cases = json.load(f)

# compare replica24_2 and oct13 cases
for c in cases:
    if c['id'] in ['replica24_1', 'replica24_2'] or 'oct13' in c['id']:
        ohlc = c['OHLC']
        highs = [x['high'] for x in ohlc]
        lows = [x['low'] for x in ohlc]
        opens = [x['open'] for x in ohlc]
        closes = [x['close'] for x in ohlc]
        rng = max(highs) - min(lows)
        sp = (opens[0] - min(lows)) / rng
        ep = (closes[-1] - min(lows)) / rng
        print(f"ID: {c['id'][:20]:20s} | C={c['C']:5.1f} | rng={rng:5.2f} | sp={sp:5.2f} | ep={ep:5.2f} | dir={'BULL' if closes[-1]>opens[0] else 'BEAR'}")
