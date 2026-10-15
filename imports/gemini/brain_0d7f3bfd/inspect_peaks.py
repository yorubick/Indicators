import json
import numpy as np
from datetime import datetime, timezone

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

target_ids = [
    ("14:00 -> 14:22 (C=83)", lambda c: c['START'].startswith("2026-10-12T14:00") and c['bars'] == 23),
    ("15:28 -> 15:50 (C=81)", lambda c: c['START'].startswith("2026-10-12T15:28") and c['bars'] == 23),
    ("15:27 -> 15:51 (C=93)", lambda c: c['START'].startswith("2026-10-12T15:27") and c['bars'] == 25),
    ("13-19:00 -> 19:20 (C=81)", lambda c: c['START'].startswith("2026-10-13T19:00") and c['bars'] == 21),
    ("15:28 -> 15:52 (C=81)", lambda c: c['START'].startswith("2026-10-12T15:28") and c['bars'] == 25),
    ("14:00 -> 14:21 (C=62 control)", lambda c: c['START'].startswith("2026-10-12T14:00") and c['bars'] == 22),
    ("15:27 -> 15:50 (C=69 control)", lambda c: c['START'].startswith("2026-10-12T15:27") and c['bars'] == 24),
]

for label, predicate in target_ids:
    c = next(x for x in data['cases'] if predicate(x))
    ohlc = c['OHLC']
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    opens = [x['open'] for x in ohlc]
    
    rng = max(highs) - min(lows)
    imax = highs.index(max(highs))
    imin = lows.index(min(lows))
    
    print(f"\n================ {label} ================")
    print(f"START: {c['START']}, END: {c['END']}, bars: {c['bars']}, dt: {c['dt']}, C: {c['C']}")
    print(f"Global High: {max(highs)} at bar {imax} ({imax - len(highs)} from end)")
    print(f"Global Low:  {min(lows)} at bar {imin} ({imin - len(lows)} from end)")
    print(f"Range: {rng:.2f} pts ({rng / 0.25:.0f} ticks)")
    print(f"End bar OHLC: O={opens[-1]}, H={highs[-1]}, L={lows[-1]}, C={closes[-1]}")
    print(f"Start bar OHLC: O={opens[0]}, H={highs[0]}, L={lows[0]}, C={closes[0]}")
    
    # Check if end bar made new high or low
    prev_max = max(highs[:-1])
    prev_min = min(lows[:-1])
    is_new_h = highs[-1] > prev_max
    is_new_l = lows[-1] < prev_min
    print(f"End bar new high? {is_new_h} (prev max={prev_max}, end H={highs[-1]})")
    print(f"End bar new low?  {is_new_l} (prev min={prev_min}, end L={lows[-1]})")
