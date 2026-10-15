import csv, datetime
from pathlib import Path

p = Path('G:/trading/guias/analisis/manual/Lite_0445_051500_1m_a.csv')
rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))
candles = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

for end_str, C in [('04:50:00', 60), ('05:00:00', 60), ('05:05:00', 75), ('05:15:00', 116), ('05:25:00', 113), ('05:30:00', 110)]:
    sub = [candles[t] for t in range(ts('04:45:00'), ts(end_str) + 60, 60) if t in candles]
    highs = [x['high'] for x in sub]
    lows = [x['low'] for x in sub]
    closes = [x['close'] for x in sub]
    opens = [x['open'] for x in sub]
    h = max(highs)
    l = min(lows)
    ranges = [x['high'] - x['low'] for x in sub]
    print(f"END {end_str}: bars={len(sub)}, C={C}")
    print(f"  H={h}, L={l}, Range={h-l}")
    print(f"  First bar: O={opens[0]}, H={highs[0]}, L={lows[0]}, C={closes[0]}")
    print(f"  Last bar:  O={opens[-1]}, H={highs[-1]}, L={lows[-1]}, C={closes[-1]}")
    print(f"  Idx of Max H: {highs.index(h)}/{len(sub)-1}, Idx of Min L: {lows.index(l)}/{len(sub)-1}")
