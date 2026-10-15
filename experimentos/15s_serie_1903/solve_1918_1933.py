from scipy.optimize import brentq
import numpy as np

# Script to solve C for START 19:18, END 19:33, Eval 19:34
# Edit the observed values below when reported by TradingView
obs = {
    "Lane 1 A": 30888.48,
    "Lane 1 B": 30887.05,
    "Lane 2 A": 30882.12,
    "Lane 2 B": 30881.27,
    "Lane 3 A": 30878.90,
    "Lane 3 B": 30878.55,
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

def solve(observations):
    solved = {}
    for lane, val in observations.items():
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
    
    print(f"\n--- Simulación con C = {int_c} ---")
    max_err = 0.0
    for lane, val in observations.items():
        b0 = factors[lane]
        alpha = 2.0 / ((b0 * int_c / dt) + 1.0)
        st = seed
        for cl in closes:
            st += alpha * (cl - st)
        err = abs(st - val)
        if err > max_err: max_err = err
        print(f"  {lane:<9}: Sim = {st:.2f} | Obs = {val:.2f} | Err = {err:.4f}")
    print(f"  Error máximo con C={int_c}: {max_err:.4f} pts")
    return int_c, mean_c, max_err

if __name__ == "__main__":
    print("=== SCRIPT LISTO PARA INVERSIÓN START 19:18, END 19:33 ===")
    solve(obs)
