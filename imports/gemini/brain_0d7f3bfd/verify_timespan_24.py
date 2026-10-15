# Test the formula C = (n - 1) * dt / 24

for n in [21, 22, 23, 24, 25]:
    dt = 60
    t_span = (n - 1) * dt
    c_val = t_span / 24.0
    print(f"n={n}: t_span={t_span}s -> c = {c_val:.4f} -> round={round(c_val)}, floor={int(c_val)}")
