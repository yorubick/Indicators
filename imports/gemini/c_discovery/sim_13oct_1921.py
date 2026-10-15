# Prediction for 2026-10-13: START 19:00, END 19:21, eval on 19:22 UTC

dt = 60.0
# END 19:21: High is 30770.25, Low is 30757.50.
# Breakout is UP (High of 19:21 broke previous high).
# Seed is Low of END bar (19:21) = 30757.50
seed = 30757.50

# Candle 19:22 UTC:
# Open 30769.75, High 30771.00, Low 30767.00, Close 30768.75
close_1922 = 30768.75

lanes = {
    "Lane 3 A": 24.0,
    "Lane 3 B": 89.0 / 3.0,
    "Lane 2 A": 8.0,
    "Lane 2 B": 89.0 / 9.0,
    "Lane 1 A": 72.0 / 27.0,
    "Lane 1 B": 89.0 / 27.0,
}

cands = [75, 81, 84, 102, 112]

print("--- 2026-10-13: START 19:00, END 19:21, eval 19:22 UTC ---")
print(f"{'C':4} | {'Lane 3 A':9} | {'Lane 3 B':9} | {'Lane 2 A':9} | {'Lane 2 B':9} | {'Lane 1 A':9} | {'Lane 1 B':9}")
print("-" * 75)

for c in cands:
    vals = {}
    for name, b0 in lanes.items():
        alpha = 2.0 / ((b0 * c / dt) + 1.0)
        st = seed + alpha * (close_1922 - seed)
        vals[name] = st
    print(f"{c:4d} | {vals['Lane 3 A']:9.2f} | {vals['Lane 3 B']:9.2f} | {vals['Lane 2 A']:9.2f} | {vals['Lane 2 B']:9.2f} | {vals['Lane 1 A']:9.2f} | {vals['Lane 1 B']:9.2f}")
