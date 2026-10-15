import json, csv
from pathlib import Path

# Load all 21-bar cases available
cases_21 = [
    # Morning 12 Oct
    {'start': '04:45:00', 'end': '05:05:00', 'C': 75.0, 'date': '2026-10-12', 'notes': 'morning 12 oct'},
    {'start': '06:00:00', 'end': '06:20:00', 'C': 77.0, 'date': '2026-10-12', 'notes': 'bajista 06:00'},
    {'start': '07:00:00', 'end': '07:20:00', 'C': 75.0, 'date': '2026-10-12', 'notes': 'lateral 07:00'},
    {'start': '14:00:00', 'end': '14:20:00', 'C': 62.0, 'date': '2026-10-12', 'notes': 'bajista 14:00'},
    {'start': '15:30:00', 'end': '15:50:00', 'C': 69.0, 'date': '2026-10-12', 'notes': 'alcista 15:30'},
    # Evening 12 Oct
    {'start': '19:00:00', 'end': '19:20:00', 'C': 77.0, 'date': '2026-10-12', 'notes': 'evening 19:00'},
    {'start': '19:01:00', 'end': '19:21:00', 'C': 77.0, 'date': '2026-10-12', 'notes': 'evening 19:01'},
    {'start': '19:02:00', 'end': '19:22:00', 'C': 50.0, 'date': '2026-10-12', 'notes': 'evening 19:02'},
    {'start': '19:03:00', 'end': '19:23:00', 'C': 50.0, 'date': '2026-10-12', 'notes': 'evening 19:03'},
    {'start': '19:04:00', 'end': '19:24:00', 'C': 50.0, 'date': '2026-10-12', 'notes': 'evening 19:04'},
    {'start': '19:11:00', 'end': '19:31:00', 'C': 80.0, 'date': '2026-10-12', 'notes': 'evening 19:11'},
    # Evening 13 Oct
    {'start': '19:00:00', 'end': '19:20:00', 'C': 81.0, 'date': '2026-10-13', 'notes': 'evening 13 oct'},
]

# Let's inspect the 1m CSV data to get OHLC for each of these 21-bar windows
ref_1m_path = Path('G:/trading/guias/analisis/character_manual_15m_1m.csv')
rows_1m = list(csv.DictReader(ref_1m_path.open(encoding='utf-8-sig')))
c_1m = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_1m}

def ts(s_str, date):
    from datetime import datetime
    return int(datetime.fromisoformat(f"{date}T{s_str}+00:00").timestamp())

print("=== ALL 12 CASES OF EXACTLY 21 BARS (1m SOURCE) ===")
print(f"{'Date':<10} {'START':<9} {'END':<9} {'C':<5} {'High':<9} {'Low':<9} {'Range_pts':<10} {'Ticks':<6} {'NetMove':<9} {'ER':<8} {'Notes':<18}")

for c in cases_21:
    t_s = ts(c['start'], c['date'])
    t_e = ts(c['end'], c['date'])
    sub = [c_1m[t] for t in range(t_s, t_e + 1, 60) if t in c_1m]
    if sub:
        highs = [x['high'] for x in sub]
        lows = [x['low'] for x in sub]
        closes = [x['close'] for x in sub]
        H = max(highs)
        L = min(lows)
        R = H - L
        ticks = round(R * 4)
        net_move = closes[-1] - sub[0]['open']
        abs_diffs = sum(abs(closes[i] - closes[i-1]) for i in range(1, len(closes)))
        er = abs(closes[-1] - sub[0]['open']) / abs_diffs if abs_diffs > 0 else 0
        print(f"{c['date']:<10} {c['start']:<9} {c['end']:<9} {c['C']:<5.1f} {H:<9.2f} {L:<9.2f} {R:<10.2f} {ticks:<6d} {net_move:<9.2f} {er:<8.4f} {c['notes']:<18}")
    else:
        print(f"{c['date']:<10} {c['start']:<9} {c['end']:<9} {c['C']:<5.1f} {'[No data in character_manual_15m_1m.csv]':<40} {c['notes']:<18}")
