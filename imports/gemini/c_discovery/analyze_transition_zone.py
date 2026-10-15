import pandas as pd
import numpy as np
import tabulate_1s_structural_features as t1s

df = t1s.df[t1s.df['n'] >= 21].copy()

# Let's inspect the transition zone: n between 30 and 37
transition_df = df[(df['n'] >= 30) & (df['n'] <= 37)][['id', 'n', 'C_int', 'close', 'range', 'pos_range', 'dist_ext', 'n/18.3', 'bs_low']]
print("Transition zone cases (n = 30..37):")
print(transition_df.to_string(index=False))

# Let's evaluate potential predictors:
# Let x = n / 18.3
# Look at pos_range:
# For n=33 (140400_n33), pos_range = 0.0301, C = 2
# For n=34 (140400_n34), pos_range = 0.1265, C = 1
# For n=35 (140400_n35), pos_range = 0.1145, C = 1
# For n=36 (140400_n36), pos_range = 0.1807, C = 2
# For n=37 (140400_n37), pos_range = 0.3434, C = 2

# Notice: What if C is:
# C = floor(n / 18.3 + delta_C)?
# What is delta_C?
# At n=33: n/18.3 = 1.803. If delta_C >= 0.20 (i.e. 2 - 1.803 = 0.197), then floor(1.803 + 0.197) = 2.
# At n=34: n/18.3 = 1.858. If delta_C < 0.142, then floor(1.858 + delta_C) = 1.
# At n=35: n/18.3 = 1.913. If delta_C < 0.087, then floor(1.913 + delta_C) = 1.
# At n=36: n/18.3 = 1.967. If delta_C >= 0.033, then floor(1.967 + 0.033) = 2.

print("\nRequired delta_C to produce C=2 for each n:")
for idx, r in transition_df.iterrows():
    req = 2.0 - r['n/18.3']
    print(f"id: {r['id']}, n: {r['n']}, C: {r['C_int']}, req_delta: {req:.4f}, dist_ext: {r['dist_ext']:.4f}, pos_range: {r['pos_range']:.4f}")
