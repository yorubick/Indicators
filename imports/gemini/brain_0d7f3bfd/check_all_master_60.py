import master_cases

print("=== CHECKING TICKS & BARS ACROSS ALL MASTER CASES (TF=60) ===")
print(f"{'Case':<22} {'B':<4} {'R_pts':<7} {'Ticks':<6} {'C':<6} {'T+B':<6} {'T-B':<6} {'C-T':<6} {'C/T':<6} {'C/B':<6}")
for d in master_cases.dataset:
    if d['dt'] != 60 or d['bars'] < 21: continue
    s = d['s']
    e = d['e']
    B = d['bars']
    R = d['range']
    T = round(R * 4)
    C = d['C']
    c_t = f"{C/T:.2f}" if T > 0 else "0"
    c_b = f"{C/B:.2f}" if B > 0 else "0"
    print(f"{s}->{e:<8} {B:<4d} {R:<7.2f} {T:<6d} {C:<6.1f} {T+B:<6d} {T-B:<6d} {C-T:<6.1f} {c_t:<6} {c_b:<6}")
