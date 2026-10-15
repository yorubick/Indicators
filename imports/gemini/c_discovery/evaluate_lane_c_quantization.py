# Test quantization on Lane C: N_C = (8/3) * C / dt
# In 1m (dt = 60): C = N_C * 60 / (8/3) = N_C * 22.5
# In 15s (dt = 15): C = N_C * 15 / (8/3) = N_C * 5.625

import numpy as np

c_1m_cases = [50, 52, 71, 88, 112, 130, 135, 136]
c_15s_cases = [67, 79, 87, 88, 102, 106, 123]

print("=== LANE C QUANTIZATION IN 1M (dt = 60s, step = 22.5s) ===")
for c in c_1m_cases:
    n_c = (8.0 / 3.0) * c / 60.0
    c_recon = round(n_c) * 22.5
    print(f"C={c:>3} -> N_C = {n_c:>6.3f} | round(N_C) = {round(n_c):>2} -> C_recon = {c_recon:>5.1f} (err: {abs(c - c_recon):>4.1f})")

print("\n=== LANE C QUANTIZATION IN 15S (dt = 15s, step = 5.625s) ===")
for c in c_15s_cases:
    n_c = (8.0 / 3.0) * c / 15.0
    c_recon = round(n_c) * 5.625
    print(f"C={c:>3} -> N_C = {n_c:>6.3f} | round(N_C) = {round(n_c):>2} -> C_recon = {c_recon:>5.1f} (err: {abs(c - c_recon):>4.1f})")
