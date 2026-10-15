# Exact curve values for END 19:34, evaluated at candle 19:35 and 19:36 UTC

dt = 60.0
seed = 30885.75 # Low of 19:34 bar
close_1935 = 30904.25 # Close of 19:35 bar
close_1936 = 30908.25 # Close of 19:36 bar

lanes = {
    "Lane 3 A": 24.0,
    "Lane 3 B": 89.0 / 3.0,
    "Lane 2 A": 8.0,
    "Lane 2 B": 89.0 / 9.0,
    "Lane 1 A": 72.0 / 27.0,
    "Lane 1 B": 89.0 / 27.0,
}

c_candidates = [88, 109, 112, 130, 135, 136]

print("--- EVALUATION ON CANDLE 19:35 UTC (1 bar post-END) ---")
print(f"{'C':4} | {'Lane 3 A':9} | {'Lane 3 B':9} | {'Lane 2 A':9} | {'Lane 2 B':9} | {'Lane 1 A':9} | {'Lane 1 B':9}")
print("-" * 75)

for c in c_candidates:
    vals = {}
    for name, b0 in lanes.items():
        alpha = 2.0 / ((b0 * c / dt) + 1.0)
        st = seed + alpha * (close_1935 - seed)
        vals[name] = st
    print(f"{c:4d} | {vals['Lane 3 A']:9.2f} | {vals['Lane 3 B']:9.2f} | {vals['Lane 2 A']:9.2f} | {vals['Lane 2 B']:9.2f} | {vals['Lane 1 A']:9.2f} | {vals['Lane 1 B']:9.2f}")

print("\n--- EVALUATION ON CANDLE 19:36 UTC (2 bars post-END) ---")
print(f"{'C':4} | {'Lane 3 A':9} | {'Lane 3 B':9} | {'Lane 2 A':9} | {'Lane 2 B':9} | {'Lane 1 A':9} | {'Lane 1 B':9}")
print("-" * 75)

for c in c_candidates:
    vals = {}
    for name, b0 in lanes.items():
        alpha = 2.0 / ((b0 * c / dt) + 1.0)
        st = seed + alpha * (close_1935 - seed)
        st = st + alpha * (close_1936 - st)
        vals[name] = st
    print(f"{c:4d} | {vals['Lane 3 A']:9.2f} | {vals['Lane 3 B']:9.2f} | {vals['Lane 2 A']:9.2f} | {vals['Lane 2 B']:9.2f} | {vals['Lane 1 A']:9.2f} | {vals['Lane 1 B']:9.2f}")
