import csv, json
import numpy as np

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

# Case 1: 19:04 -> 19:29 (C=134)
c1904_29 = next(c for c in data['cases'] if c['START'].startswith('2026-10-12T19:04') and c['bars'] == 26)

# Case 2: 19:04 -> 19:30 (C=109)
c1904_30 = next(c for c in data['cases'] if c['START'].startswith('2026-10-12T19:04') and c['bars'] == 27)

# Case 3: 19:04 -> 19:28 (C=128)
c1904_28 = next(c for c in data['cases'] if c['START'].startswith('2026-10-12T19:04') and c['bars'] == 25)

# Load 18:50..19:20 from seven_cloud_1m.csv
with open(r'G:\trading\guias\analisis\seven_cloud_1m.csv') as f:
    all_1m = list(csv.DictReader(f))

time_map = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in all_1m}

def get_ohlc(start_ts, end_ts):
    return [time_map[t] for t in range(start_ts, end_ts + 60, 60) if t in time_map]

import datetime
def ts(s): return int(datetime.datetime.fromisoformat(f'2026-10-12T{s}+00:00').timestamp())

c1854 = get_ohlc(ts('18:54:00'), ts('19:20:00'))
c1855 = get_ohlc(ts('18:55:00'), ts('19:20:00'))
c1856 = get_ohlc(ts('18:56:00'), ts('19:20:00'))

cases_to_compare = [
    ("18:54 -> 19:20 (C=134)", c1854, 134),
    ("19:04 -> 19:29 (C=134)", c1904_29['OHLC'], 134),
    ("18:56 -> 19:20 (C=109)", c1856, 109),
    ("19:04 -> 19:30 (C=109)", c1904_30['OHLC'], 109),
    ("18:55 -> 19:20 (C=62)",  c1855, 62),
    ("19:04 -> 19:28 (C=128)", c1904_28['OHLC'], 128),
]

print(f"{'Label':24s} | n  | High   | Low    | Rng   | Start O | End C  | Net   | High-to-End | Low-to-End")
print("-" * 95)
for label, ohlc, C in cases_to_compare:
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    h_max = max(highs)
    l_min = min(lows)
    imax = highs.index(h_max)
    imin = lows.index(l_min)
    n = len(ohlc)
    dist_h = n - 1 - imax
    dist_l = n - 1 - imin
    net = ohlc[-1]['close'] - ohlc[0]['open']
    print(f"{label:24s} | {n:2d} | {h_max:7.2f} | {l_min:7.2f} | {h_max-l_min:5.2f} | {ohlc[0]['open']:7.2f} | {ohlc[-1]['close']:7.2f} | {net:5.2f} | {dist_h:11d} | {dist_l:10d}")
