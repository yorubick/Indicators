import csv, datetime
from pathlib import Path
import numpy as np

ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

end_sweep_cases = [
    ('19:18:00', 88),
    ('19:19:00', 115),
    ('19:20:00', 106),
    ('19:20:15', 79),
    ('19:20:30', 67),
    ('19:20:45', 66),
    ('19:21:00', 115),
    ('19:21:15', 106),
    ('19:21:30', 79),
    ('19:21:45', 66),
    ('19:22:00', 106),
]

t_start = ts('18:55:00')

print("END sweep: candle position within range vs C:")
print(f"{'END':<10} | {'C':>3} | {'H_tot':>8} | {'L_tot':>8} | {'Rng':>5} | {'END C':>8} | {'END pos':>7} | {'END H-L':>7}")
print("-" * 75)

for e_str, C in end_sweep_cases:
    t_e = ts(e_str)
    sub = [candles_15s[t] for t in range(t_start, t_e + 15, 15) if t in candles_15s]
    h_tot = max(b['high'] for b in sub)
    l_tot = min(b['low'] for b in sub)
    rng_tot = h_tot - l_tot
    end_c = sub[-1]['close']
    end_pos = (end_c - l_tot) / rng_tot
    end_bar_rng = sub[-1]['high'] - sub[-1]['low']
    print(f"{e_str:<10} | {C:3d} | {h_tot:8.2f} | {l_tot:8.2f} | {rng_tot:5.2f} | {end_c:8.2f} | {end_pos:7.3f} | {end_bar_rng:7.2f}")
