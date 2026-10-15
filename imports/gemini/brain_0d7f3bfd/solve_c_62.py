import csv
from datetime import datetime, timezone

with open('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

by_time = {int(r['time']): {k: float(r[k]) for k in ('open', 'high', 'low', 'close')} for r in rows}

def ts(t_str):
    return int(datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

# Case A: START 19:03:15, END 19:23:30, dt = 15
t_start = ts('19:03:15')
t_end = ts('19:23:30')

bars = [by_time[t] for t in range(t_start, t_end + 15, 15) if t in by_time]
print(f"Total bars: {len(bars)}")
start_open = bars[0]['open']
end_close = bars[-1]['close']
rng_high = max(b['high'] for b in bars)
rng_low = min(b['low'] for b in bars)
rng_pts = rng_high - rng_low
bar_cnt = len(bars)
close = end_close
open_ = bars[-1]['open']

print(f"start_open: {start_open}")
print(f"end_close: {end_close}, end_open: {open_}")
print(f"rng_high: {rng_high}, rng_low: {rng_low}, rng_pts: {rng_pts}")

# Now let's test why user got C = 62 or what produced 30868.31 / 30868.29!
# Let's solve what C produces Lane 3 A = 30868.31 and Lane 3 B = 30868.29!
target_l3a = 30868.31
target_l3b = 30868.29
t_target = ts('19:26:45')

print("\n--- SOLVING FOR C FROM THE OBSERVED VALUES (Lane 3 A: 30868.31, Lane 3 B: 30868.29) ---")
# What was the seed?
# In bullish breakout, seed is end_low or end_high or start_open?
for seed_name, seed in [('end_low', bars[-1]['low']), ('end_high', bars[-1]['high']), ('rng_low', rng_low), ('end_close', end_close)]:
    for dt in [15, 60]:
        for c in range(10, 150):
            len_l3a = (72.0 / 3.0) * (c / dt)
            len_l3b = (89.0 / 3.0) * (c / dt)
            a_l3a = 2.0 / (len_l3a + 1.0)
            a_l3b = 2.0 / (len_l3b + 1.0)
            va, vb = seed, seed
            for t in range(t_end + 15, t_target + 15, 15):
                cl = by_time[t]['close']
                va += a_l3a * (cl - va)
                vb += a_l3b * (cl - vb)
            err = abs(va - target_l3a) + abs(vb - target_l3b)
            if err < 0.05:
                print(f"Seed={seed_name} ({seed}), dt={dt}, C={c}: L3A={va:.2f}, L3B={vb:.2f}, err={err:.4f}")
