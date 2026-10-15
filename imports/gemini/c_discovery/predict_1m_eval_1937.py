# 1m source prediction for END 19:36 eval 19:37
seed = 30902.25
close_37 = 30906.25
dt = 60.0

factors = {
    "Lane 3 A": 24.0,           # Lane A Fast
    "Lane 3 B": 89.0 / 3.0,     # Lane A Slow
    "Lane 2 A": 8.0,            # Lane B Fast
    "Lane 2 B": 89.0 / 9.0,     # Lane B Slow
    "Lane 1 A": 72.0 / 27.0,    # Lane C Fast
    "Lane 1 B": 89.0 / 27.0,    # Lane C Slow
}

print("=== PREDICCIÓN EN 1M SOURCE PARA END = 19:36, EVAL = 19:37 ===")
for c_cand in [112, 135]:
    print(f"\n--- Si C_1m = {c_cand} ---")
    for lane, b0 in factors.items():
        alpha = 2.0 / ((b0 * c_cand / dt) + 1.0)
        st = seed + alpha * (close_37 - seed)
        print(f"  {lane:<9}: {st:.2f}")
