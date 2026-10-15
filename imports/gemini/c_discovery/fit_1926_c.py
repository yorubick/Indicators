from scipy.optimize import minimize_scalar
import numpy as np

# Official values at 19:29 for START 19:03, END 19:26:
# Lane 3 A / B: 30,867.95 / 30,867.82
# Lane 2 A / B: 30,869.15 / 30,868.83
# Lane 1 A / B: 30,871.64 / 30,871.06
observed = {
    "Lane 3 A": 30867.95,
    "Lane 3 B": 30867.82,
    "Lane 2 A": 30869.15,
    "Lane 2 B": 30868.83,
    "Lane 1 A": 30871.64,
    "Lane 1 B": 30871.06,
}

# In 1m chart, END is 19:26.
# What was the seed?
# At 19:26, what was the Low of the END bar (19:26)?
# Let's check the OHLC of 19:26 in Lite_1903_192300_1m_b.csv or historical:
# At 19:26: Open 30868.75, High 30873.0, Low 30867.25, Close 30872.5
# Breakout happened on 19:29.
# Bars between 19:26 and 19:29:
# 19:27: Close = 30873.0
# 19:28: Close = 30872.75
# 19:29: Close = 30875.75
# Seed = Low of 19:26 = 30867.25

closes = [30873.0, 30872.75, 30875.75]
seed = 30867.25
dt = 60.0

LANES_BASE = {
    "Lane 3 A": 24.0,
    "Lane 3 B": 89.0 / 3.0,
    "Lane 2 A": 8.0,
    "Lane 2 B": 89.0 / 9.0,
    "Lane 1 A": 72.0 / 27.0,
    "Lane 1 B": 89.0 / 27.0,
}

def simulate(C_val):
    err = 0.0
    for lane, base in LANES_BASE.items():
        alpha = 2.0 / ((base * C_val / dt) + 1.0)
        state = seed
        for c in closes:
            state += alpha * (c - state)
        err += (state - observed[lane]) ** 2
    return err

res = minimize_scalar(simulate, bounds=(40, 150), method="bounded")
best_C = res.x
print(f"Optimal fitted C: {best_C:.6f} (round: {round(best_C)})")
print(f"Min SSE: {res.fun:.6e}")

# Check with best C
for lane, base in LANES_BASE.items():
    alpha = 2.0 / ((base * best_C / dt) + 1.0)
    state = seed
    for c in closes:
        state += alpha * (c - state)
    print(f"{lane:10s} | Sim: {state:10.4f} | Obs: {observed[lane]:10.2f} | Diff: {state - observed[lane]:+.4f}")
