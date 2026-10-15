import pandas as pd
import numpy as np
import tabulate_1s_structural_features as t1s

df = t1s.df[t1s.df['n'] >= 21].copy()

# We want an operator C = floor(x_eff) or round(x_eff) that is continuous, physical, and achieves 100% on all 26 cases.
# Let x = n / 18.3.
# Let's inspect x for all cases:
# n=21..32: x in [1.148, 1.749], C = 1
# n=33 (dist_ext=0.0301): x = 1.803, C = 2
# n=33 (dist_ext=0.1265): x = 1.803, C = 1
# n=34 (dist_ext=0.1265): x = 1.858, C = 1
# n=35 (dist_ext=0.1145): x = 1.913, C = 1
# n=36 (dist_ext=0.1807): x = 1.967, C = 2
# n=37..40: x in [2.022, 2.186], C = 2

# Consider a physical model based on Failure Swing:
# In SMC/ICT, Failure Swing (FS) is defined as price retracing back from the extreme by more than a threshold tau_FS.
# If price has NOT failed (is still within tau_FS of the extreme), the leg is expanding / active impulse.
# If price has retraced > tau_FS, it is in failure / pullback.

# Let's test a simple expansion modulation:
# If price is within the breakout band (dist_ext < 0.05):
#   effective expansion boost = +0.20
# Else:
#   effective expansion boost = 0
# With boost:
# at n=33, dist_ext = 0.0301 -> x_eff = 1.803 + 0.20 = 2.003 -> floor(2.003) = 2!
# at n=32, dist_ext = 0.0301 -> x_eff = 1.749 + 0.20 = 1.949 -> floor(1.949) = 1! (STILL 1!)
# at n=33, dist_ext = 0.1265 -> x_eff = 1.803 + 0.00 = 1.803 -> floor(1.803) = 1!
# at n=34, dist_ext = 0.1265 -> x_eff = 1.858 + 0.00 = 1.858 -> floor(1.858) = 1!
# at n=35, dist_ext = 0.1145 -> x_eff = 1.913 + 0.00 = 1.913 -> floor(1.913) = 1!
# at n=36, x = 1.967. Wait! At n=36, C=2, but dist_ext = 0.1807! Why is n=36 C=2?
# Notice: 36 / 18.3 = 1.9672. If the natural transition threshold is round(x), 1.9672 rounds to 2!
# Or if tau_base = 36 / 18.3 = 1.967 >= 1.967?
# Let's test if C = floor(x + 0.05) or round(x) or what!

print("Testing candidates across all 26 cases:")

# Candidate 1: Floor with Failure Swing Boost
# x_eff = (n / 18.3) + (0.20 if dist_ext < 0.05 else 0.0)
# But what about n=36? At n=36, x = 1.9672. If threshold is 1.95 (i.e. n >= 36), it becomes 2.
# In Pine Script: what if 36 is the boundary? Remember 36 = 18 * 2 = 2 cycles!
# In Pine Script, 36 bars / 18 bars = 2.0!

for base_ratio in [18.0, 18.25, 18.3, 18.333]:
    for boost in [0.15, 0.20, 0.22]:
        for d_th in [0.04, 0.05, 0.06]:
            preds = []
            for _, r in df.iterrows():
                n = r['n']
                d = r['dist_ext']
                # if n / base_ratio >= 2.0, or n >= 36:
                # or continuous formula:
                x = n / base_ratio
                b = boost if d < d_th else 0.0
                pred = int(np.floor(x + b))
                # Also if round is used:
                preds.append(pred)
            matches = (np.array(preds) == df['C_int'].values).sum()
            if matches >= 25:
                print(f"base_ratio={base_ratio}, boost={boost}, d_th={d_th} -> Matches: {matches} / {len(df)}")

