import master_cases
import numpy as np

# Load all 42 cases from master_cases
dataset = master_cases.dataset

print(f"Total dataset cases: {len(dataset)}")

# Separate cases into n < 21 and n >= 21
cases_short = [d for d in dataset if d['bars'] < 21]
cases_long = [d for d in dataset if d['bars'] >= 21]

print(f"Short cases (n < 21): {len(cases_short)} (Solved: C = max(dt, n * dt * 10 / 183))")
print(f"Long cases (n >= 21): {len(cases_long)}")

# Let's inspect the target C values in long cases:
c_long_vals = sorted(list(set(d['C'] for d in cases_long)))
print("Unique C values in long cases:", c_long_vals)

# For each unique C value, let's see which cases produce it:
for val in c_long_vals:
    matching = [d for d in cases_long if d['C'] == val]
    print(f"\n--- C = {val} ({len(matching)} cases) ---")
    for m in matching:
        sub = m['sub']
        highs = [b['high'] for b in sub]
        lows = [b['low'] for b in sub]
        closes = [b['close'] for b in sub]
        opens = [b['open'] for b in sub]
        
        # Key metrics:
        rng = max(highs) - min(lows)
        # End bar retracement
        end_ret = (max(highs) - closes[-1]) / rng if rng > 0 else 0
        # Start bar relative position
        start_pos = (opens[0] - min(lows)) / rng if rng > 0 else 0
        # Trend direction
        trend = "UP" if closes[-1] > opens[0] else "DOWN"
        
        print(f"  {m['s'][:5]}->{m['e'][:8]} (dt={m['dt']:2d}, n={m['bars']:3d}) | Rng={rng:5.2f} | Trend={trend} | EndRet={end_ret:5.2f} | StartPos={start_pos:5.2f}")
