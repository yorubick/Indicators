import csv
from pathlib import Path
from datetime import datetime, timezone

ref_1m_path = Path('G:/trading/guias/analisis/character_manual_15m_1m.csv')
rows_1m = list(csv.DictReader(ref_1m_path.open(encoding='utf-8-sig')))
candles_1m = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_1m}

def ts(dt_str, date="2026-10-12"):
    return int(datetime.fromisoformat(f"{date}T{dt_str}+00:00").timestamp())

print("=== CHECKING COVERAGE IN character_manual_15m_1m.csv ===")

# Window 1: 07:00 (06:50 to 07:30)
t_0650 = ts('06:50:00')
t_0730 = ts('07:30:00')
count_0700 = sum(1 for t in range(t_0650, t_0730 + 1, 60) if t in candles_1m)
print(f"Candles available around 07:00 (06:50 to 07:30): {count_0700} / 41")

# Window 2: 15:30 (15:20 to 16:00)
t_1520 = ts('15:20:00')
t_1600 = ts('16:00:00')
count_1530 = sum(1 for t in range(t_1520, t_1600 + 1, 60) if t in candles_1m)
print(f"Candles available around 15:30 (15:20 to 16:00): {count_1530} / 41")
