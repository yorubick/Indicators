import csv, datetime
from pathlib import Path

ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

start_cases = [
    ('18:54:00', 123),
    ('18:54:15', 118),
    ('18:54:30', 67),
    ('18:54:45', 67),
    ('18:55:00', 106),
    ('18:55:15', 66),
    ('18:55:30', 88),
    ('18:55:45', 88),
    ('18:56:00', 106),
    ('18:56:15', 67),
    ('18:56:30', 67),
    ('18:56:45', 79),
    ('18:57:00', 67),
]

t_end = ts('19:20:00')

print(f"{'START':<9} | {'C':>3} | {'B0 C-O':>6} | {'B0 H-L':>6} | {'H(0..3)-L(0..3)':>15} | {'H(0..5)-L(0..5)':>15}")
print("-" * 75)
for s_str, C in start_cases:
    t_s = ts(s_str)
    sub = [candles[t] for t in range(t_s, t_end + 15, 15) if t in candles]
    h0_3 = max(b['high'] for b in sub[:4]) - min(b['low'] for b in sub[:4])
    h0_5 = max(b['high'] for b in sub[:6]) - min(b['low'] for b in sub[:6])
    b0_diff = sub[0]['close'] - sub[0]['open']
    b0_rng = sub[0]['high'] - sub[0]['low']
    print(f"{s_str:<9} | {C:3d} | {b0_diff:6.2f} | {b0_rng:6.2f} | {h0_3:15.2f} | {h0_5:15.2f}")
