import csv, datetime
from pathlib import Path

# Case 1: Morning 04:45 - 05:05 (21 bars) -> C = 75
p_m = Path('G:/trading/guias/analisis/manual/Lite_0445_050500_1m_a.csv')
rows_m = list(csv.DictReader(p_m.open(encoding='utf-8-sig')))
t_s_m = int(datetime.datetime.fromisoformat('2026-10-12T04:45:00+00:00').timestamp())
t_e_m = int(datetime.datetime.fromisoformat('2026-10-12T05:05:00+00:00').timestamp())
sub_m = [r for r in rows_m if t_s_m <= int(r['time']) <= t_e_m]

highs_m = [float(r['high']) for r in sub_m]
lows_m = [float(r['low']) for r in sub_m]
rng_m = max(highs_m) - min(lows_m)

# Case 2: Evening 19:00 - 19:20 (21 bars) -> C = 77
p_e = Path('G:/trading/guias/analisis/manual/Lite_1900_1920_1m_a.csv')
rows_e = list(csv.DictReader(p_e.open(encoding='utf-8-sig')))
t_s_e = int(datetime.datetime.fromisoformat('2026-10-12T19:00:00+00:00').timestamp())
t_e_e = int(datetime.datetime.fromisoformat('2026-10-12T19:20:00+00:00').timestamp())
sub_e = [r for r in rows_e if t_s_e <= int(r['time']) <= t_e_e]

highs_e = [float(r['high']) for r in sub_e]
lows_e = [float(r['low']) for r in sub_e]
rng_e = max(highs_e) - min(lows_e)

print(f"Morning 04:45-05:05 (21 bars): Range = {rng_m:.2f} pts | C = 75")
print(f"Evening 19:00-19:20 (21 bars): Range = {rng_e:.2f} pts | C = 77")
print(f"Morning 04:45-05:04 (20 bars): Range = {max([float(r['high']) for r in sub_m[:-1]]) - min([float(r['low']) for r in sub_m[:-1]]):.2f} pts | C = 65.574")
print(f"Evening 19:00-19:19 (20 bars): Range = {max([float(r['high']) for r in sub_e[:-1]]) - min([float(r['low']) for r in sub_e[:-1]]):.2f} pts | C = 65.574")
