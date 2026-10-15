from scipy.optimize import brentq
import numpy as np

# Official readings for START 19:08, END 19:33, eval 19:34
obs = {
    "Lane 1 A": 30884.72,
    "Lane 1 B": 30883.56,
    "Lane 2 A": 30880.06,
    "Lane 2 B": 30879.52,
    "Lane 3 A": 30878.09,
    "Lane 3 B": 30877.88,
}

factors = {
    "Lane 3 A": 24.0,           # Lane A Fast
    "Lane 3 B": 89.0 / 3.0,     # Lane A Slow
    "Lane 2 A": 8.0,            # Lane B Fast
    "Lane 2 B": 89.0 / 9.0,     # Lane B Slow
    "Lane 1 A": 72.0 / 27.0,    # Lane C Fast
    "Lane 1 B": 89.0 / 27.0,    # Lane C Slow
}

dt = 15.0
seed = 30877.00
closes = [30888.75, 30891.0, 30893.75, 30897.25]

print("=== INVERSIÓN EXACTA DE C PARA START 19:08, END 19:33, EVAL 19:34 ===")
solved = {}
for lane, val in obs.items():
    b0 = factors[lane]
    def sim(c_val):
        alpha = 2.0 / ((b0 * c_val / dt) + 1.0)
        st = seed
        for cl in closes:
            st += alpha * (cl - st)
        return st
    
    sol = brentq(lambda c_v: sim(c_v) - val, 10.0, 500.0)
    solved[lane] = sol
    print(f"{lane:<9}: Invertido C = {sol:.4f} (round: {round(sol)})")

vals = list(solved.values())
mean_c = np.mean(vals)
spread = max(vals) - min(vals)
int_c = round(mean_c)
print(f"\nMedia C: {mean_c:.4f} | Entero más cercano: {int_c} | Spread: {spread:.4f}")

# Simular con el entero C=70 y C=71
for c_cand in [70, 71]:
    print(f"\n--- Simulación con C = {c_cand} ---")
    max_err = 0.0
    for lane, val in obs.items():
        b0 = factors[lane]
        alpha = 2.0 / ((b0 * c_cand / dt) + 1.0)
        st = seed
        for cl in closes:
            st += alpha * (cl - st)
        err = abs(st - val)
        if err > max_err: max_err = err
        print(f"  {lane:<9}: Sim = {st:.2f} | Obs = {val:.2f} | Err = {err:.4f}")
    print(f"  Error máximo con C={c_cand}: {max_err:.4f} pts")
