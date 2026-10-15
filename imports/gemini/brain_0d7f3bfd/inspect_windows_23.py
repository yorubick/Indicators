import csv, datetime
from pathlib import Path
import numpy as np

with open(r'G:\trading\guias\analisis\seven_cloud_1m.csv') as f:
    all_1m = list(csv.DictReader(f))

time_map = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in all_1m}

def ts(s): return int(datetime.datetime.fromisoformat(f'2026-10-12T{s}+00:00').timestamp())

windows_23 = [
    ('15:26', '15:48', 82),
    ('15:27', '15:49', 82),
    ('15:28', '15:50', 81),
    ('15:29', '15:51', 75),
    ('15:30', '15:52', 68),
]

print(f"{'Window':15s} | C  | Range | Net   | Path  | ATR   | H-bar | L-bar | Dist_HL | Start_C | End_C")
print("-" * 85)

for st, en, C in windows_23:
    sub = [time_map[t] for t in range(ts(st+':00'), ts(en+':00')+60, 60) if t in time_map]
    highs = [x['high'] for x in sub]
    lows = [x['low'] for x in sub]
    closes = [x['close'] for x in sub]
    opens = [x['open'] for x in sub]
    
    rng = max(highs) - min(lows)
    net = closes[-1] - opens[0]
    path = sum(abs(closes[i] - closes[i-1]) for i in range(1, len(closes)))
    trs = [highs[0] - lows[0]] + [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, len(closes))]
    atr = np.mean(trs)
    
    imax = highs.index(max(highs))
    imin = lows.index(min(lows))
    dist_hl = abs(imax - imin)
    
    print(f"{st}->{en} | {C:2d} | {rng:5.2f} | {net:5.2f} | {path:5.2f} | {atr:5.2f} | {imax:5d} | {imin:5d} | {dist_hl:7d} | {closes[0]:7.2f} | {closes[-1]:7.2f}")
