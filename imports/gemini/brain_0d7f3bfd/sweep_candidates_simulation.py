import csv
from pathlib import Path
from datetime import datetime

ref_1m_path = Path('G:/trading/guias/analisis/character_manual_15m_1m.csv')
rows_1m = list(csv.DictReader(ref_1m_path.open(encoding='utf-8-sig')))
c_1m = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_1m}

def ts(dt_str, date="2026-10-12"):
    return int(datetime.fromisoformat(f"{date}T{dt_str}+00:00").timestamp())

print("=== SWEEP CANDIDATES: END = 15:50:00 (ALCISTA) ===")
print(f"{'START':<9} {'END':<9} {'Bars':<5} {'High':<9} {'Low':<9} {'Range':<8} {'StartO':<9} {'EndC':<9} {'StartPos':<9} {'ER':<8}")
t_end_1550 = ts('15:50:00')
for m in range(20, 36):
    start_str = f"15:{m:02d}:00"
    t_s = ts(start_str)
    sub = [c_1m[t] for t in range(t_s, t_end_1550 + 1, 60) if t in c_1m]
    if sub:
        highs = [x['high'] for x in sub]
        lows = [x['low'] for x in sub]
        closes = [x['close'] for x in sub]
        H = max(highs)
        L = min(lows)
        R = H - L
        start_o = sub[0]['open']
        end_c = closes[-1]
        start_pos = (start_o - L) / R if R > 0 else 0
        abs_diffs = sum(abs(closes[i] - closes[i-1]) for i in range(1, len(closes)))
        er = abs(end_c - start_o) / abs_diffs if abs_diffs > 0 else 0
        print(f"{start_str:<9} {'15:50:00':<9} {len(sub):<5d} {H:<9.2f} {L:<9.2f} {R:<8.2f} {start_o:<9.2f} {end_c:<9.2f} {start_pos:<9.3f} {er:<8.4f}")

print("\n=== SWEEP CANDIDATES: END = 07:20:00 (LATERAL) ===")
print(f"{'START':<9} {'END':<9} {'Bars':<5} {'High':<9} {'Low':<9} {'Range':<8} {'StartO':<9} {'EndC':<9} {'StartPos':<9} {'ER':<8}")
t_end_0720 = ts('07:20:00')
for m in range(50, 60):
    start_str = f"06:{m:02d}:00"
    t_s = ts(start_str)
    sub = [c_1m[t] for t in range(t_s, t_end_0720 + 1, 60) if t in c_1m]
    if sub:
        highs = [x['high'] for x in sub]
        lows = [x['low'] for x in sub]
        closes = [x['close'] for x in sub]
        H = max(highs)
        L = min(lows)
        R = H - L
        start_o = sub[0]['open']
        end_c = closes[-1]
        start_pos = (start_o - L) / R if R > 0 else 0
        abs_diffs = sum(abs(closes[i] - closes[i-1]) for i in range(1, len(closes)))
        er = abs(end_c - start_o) / abs_diffs if abs_diffs > 0 else 0
        print(f"{start_str:<9} {'07:20:00':<9} {len(sub):<5d} {H:<9.2f} {L:<9.2f} {R:<8.2f} {start_o:<9.2f} {end_c:<9.2f} {start_pos:<9.3f} {er:<8.4f}")

for m in range(0, 6):
    start_str = f"07:{m:02d}:00"
    t_s = ts(start_str)
    sub = [c_1m[t] for t in range(t_s, t_end_0720 + 1, 60) if t in c_1m]
    if sub:
        highs = [x['high'] for x in sub]
        lows = [x['low'] for x in sub]
        closes = [x['close'] for x in sub]
        H = max(highs)
        L = min(lows)
        R = H - L
        start_o = sub[0]['open']
        end_c = closes[-1]
        start_pos = (start_o - L) / R if R > 0 else 0
        abs_diffs = sum(abs(closes[i] - closes[i-1]) for i in range(1, len(closes)))
        er = abs(end_c - start_o) / abs_diffs if abs_diffs > 0 else 0
        print(f"{start_str:<9} {'07:20:00':<9} {len(sub):<5d} {H:<9.2f} {L:<9.2f} {R:<8.2f} {start_o:<9.2f} {end_c:<9.2f} {start_pos:<9.3f} {er:<8.4f}")
