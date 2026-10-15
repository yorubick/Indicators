import master_cases

print("=== TESTING HYPOTHESIS: C vs TICKS AND BARS ===")
print("Case                     | Bars (n) | Range pts | Ticks (4*pts) | Ticks - n | Measured C | Difference")
for d in master_cases.dataset:
    n = d['bars']
    rng_pts = d['range']
    ticks = round(rng_pts * 4)
    c_meas = d['C']
    c_pred = ticks - n
    print(f"{d['s']}->{d['e']:8s} | {n:8d} | {rng_pts:9.2f} | {ticks:13d} | {c_pred:9d} | {c_meas:10.2f} | {c_meas - c_pred:10.2f}")
