# Opción A: START 19:03, END 19:35 on 12-oct-2026, evaluated on 19:36 UTC
dt = 60.0
seed = 30895.50 # Low of 19:35 bar
close_1936 = 30908.25 # Close of 19:36 bar

lanes = {
    "Lane 3 A": 24.0,
    "Lane 3 B": 89.0 / 3.0,
    "Lane 2 A": 8.0,
    "Lane 2 B": 89.0 / 9.0,
    "Lane 1 A": 72.0 / 27.0,
    "Lane 1 B": 89.0 / 27.0,
}

cands = [88, 109, 112, 130, 135, 136]

print("--- 12-OCT-2026: START 19:03, END 19:35, eval 19:36 UTC ---")
print(f"{'C':4} | {'Lane 3 A':9} | {'Lane 3 B':9} | {'Lane 2 A':9} | {'Lane 2 B':9} | {'Lane 1 A':9} | {'Lane 1 B':9}")
print("-" * 75)

for c in cands:
    vals = {}
    for name, b0 in lanes.items():
        alpha = 2.0 / ((b0 * c / dt) + 1.0)
        st = seed + alpha * (close_1936 - seed)
        vals[name] = st
    print(f"{c:4d} | {vals['Lane 3 A']:9.2f} | {vals['Lane 3 B']:9.2f} | {vals['Lane 2 A']:9.2f} | {vals['Lane 2 B']:9.2f} | {vals['Lane 1 A']:9.2f} | {vals['Lane 1 B']:9.2f}")
