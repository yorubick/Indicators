import csv, json, datetime
from pathlib import Path

# Let's inspect the 4 cases of n = 21:
# Case 1: 12 Oct 04:45 - 05:05 (1m) -> C = 75
# Case 2: 12 Oct 19:00 - 19:20 (1m) -> C = 77
# Case 3: 13 Oct 19:00 - 19:20 (1m) -> C = 81
# Case 4: 12 Oct 19:00 - 19:05:00 (15s) -> C = 16

print("=== COMPARING THE 4 CASES OF n = 21 BARS ===")

# Load Case 3: 13 Oct 19:00 - 19:20 (1m)
p3 = Path('G:/trading/guias/analisis/manual/Lite_20261013_1900_1920_1m_c.csv')
rows3 = list(csv.DictReader(p3.open(encoding='utf-8-sig')))
t_s3 = int(datetime.datetime.fromisoformat('2026-10-13T19:00:00+00:00').timestamp())
t_e3 = int(datetime.datetime.fromisoformat('2026-10-13T19:20:00+00:00').timestamp())
sub3 = [r for r in rows3 if t_s3 <= int(r['time']) <= t_e3]
h3 = [float(r['high']) for r in sub3]
l3 = [float(r['low']) for r in sub3]
rng3 = max(h3) - min(l3)
ticks3 = round(rng3 * 4)

# Load Case 4: 12 Oct 19:00 - 19:05:00 (15s)
p4 = Path('G:/trading/guias/analisis/manual/Lite_190000_190500_15s_a.csv')
rows4 = list(csv.DictReader(p4.open(encoding='utf-8-sig')))
t_s4 = int(datetime.datetime.fromisoformat('2026-10-12T19:00:00+00:00').timestamp())
t_e4 = int(datetime.datetime.fromisoformat('2026-10-12T19:05:00+00:00').timestamp())
sub4 = [r for r in rows4 if t_s4 <= int(r['time']) <= t_e4]
h4 = [float(r['high']) for r in sub4]
l4 = [float(r['low']) for r in sub4]
rng4 = max(h4) - min(l4)
ticks4 = round(rng4 * 4)

print(f"Case 1 (12 Oct Morn 1m): n=21 | Range=24.00 pts (96 ticks) | C=75 | Ticks - n = {96 - 21}")
print(f"Case 2 (12 Oct Even 1m): n=21 | Range=24.50 pts (98 ticks) | C=77 | Ticks - n = {98 - 21}")
print(f"Case 3 (13 Oct Even 1m): n=21 | Range={rng3:.2f} pts ({ticks3} ticks) | C=81 | Ticks - n = {ticks3 - 21}")
print(f"Case 4 (12 Oct Even 15s): n=21 | Range={rng4:.2f} pts ({ticks4} ticks) | C=16 | Ticks - n = {ticks4 - 21}")
