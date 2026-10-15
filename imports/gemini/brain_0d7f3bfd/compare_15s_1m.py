import csv, datetime
from pathlib import Path
import numpy as np

# Load 15s and 1m data for 18:55:00 to 19:20:00
ref_15s = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

ref_1m = Path('G:/trading/guias/analisis/character_manual_15m_1m.csv')
rows_1m = list(csv.DictReader(ref_1m.open(encoding='utf-8-sig')))
candles_1m = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_1m}

def ts(t_str):
    return int(datetime.datetime.fromisoformat('2026-10-12T' + t_str + '+00:00').timestamp())

t_s = ts('18:55:00')
t_e = ts('19:20:00')

sub_15s = [candles_15s[t] for t in range(t_s, t_e + 1, 15) if t in candles_15s]
sub_1m = [candles_1m[t] for t in range(t_s, t_e + 1, 60) if t in candles_1m]

print(f"18:55:00 to 19:20:00:")
print(f"15s bars: {len(sub_15s)} | C = 106")
print(f"1m  bars: {len(sub_1m)} | C = 62")

# Compare High, Low, Range, Open, Close
h_15s = max(x['high'] for x in sub_15s)
l_15s = min(x['low'] for x in sub_15s)
h_1m = max(x['high'] for x in sub_1m)
l_1m = min(x['low'] for x in sub_1m)

print(f"15s High: {h_15s}, Low: {l_15s}, Range: {h_15s - l_15s}")
print(f"1m  High: {h_1m}, Low: {l_1m}, Range: {h_1m - l_1m}")

# Notice on 1m, the 19:20 candle includes up to 19:20:59!
# Let's check the last candle of 1m:
print(f"1m last candle (19:20): {sub_1m[-1]}")
print(f"15s last candle (19:20:00): {sub_15s[-1]}")
# But what if 15s includes up to 19:20:45?
sub_15s_ext = [candles_15s[t] for t in range(t_s, ts('19:20:45') + 1, 15) if t in candles_15s]
print(f"15s with END=19:20:45: High = {max(x['high'] for x in sub_15s_ext)}, Low = {min(x['low'] for x in sub_15s_ext)}, C = 66!")
