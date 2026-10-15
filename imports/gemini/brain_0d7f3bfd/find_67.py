import numpy as np

# Let's inspect the exact values for START = 18:54:30, END = 19:20:00 (dt = 15s)
import csv, datetime
from pathlib import Path

ref_15s = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s.open(encoding='utf-8-sig')))
candles = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

def ts(t_str):
    return int(datetime.datetime.fromisoformat('2026-10-12T' + t_str + '+00:00').timestamp())

t_s = ts('18:54:30')
t_e = ts('19:20:00')
dt = 15

sub = [candles[t] for t in range(t_s, t_e + 1, dt) if t in candles]
n = len(sub)
print(f"Total bars: {n}")

o = np.array([x['open'] for x in sub])
h = np.array([x['high'] for x in sub])
l = np.array([x['low'] for x in sub])
c = np.array([x['close'] for x in sub])

rng = h.max() - l.min()
print(f"Range: {rng:.2f} pts ({rng/0.25:.0f} ticks)")
print(f"Duration: {(n-1)*15} s")

# What produces 67?
# Let's check:
# 1. Any bar index?
# n = 103 bars. 103 - 67 = 36! Bar 36? Or bar 67?
print(f"Bar index 67 time: {datetime.datetime.fromtimestamp(t_s + 67*15, datetime.timezone.utc)}")
print(f"Bar from end (103 - 67 = 36) time: {datetime.datetime.fromtimestamp(t_s + 36*15, datetime.timezone.utc)}")

# Let's check prices at bar 67 and bar 36:
print(f"Bar 67: {sub[67]}")
print(f"Bar 36: {sub[36]}")
