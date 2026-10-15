import pandas as pd
import numpy as np
import tabulate_1s_structural_features as t1s

df = t1s.df[t1s.df['n'] >= 21].copy()

# Features:
# n: number of bars
# x = n / 18.3
# dist_ext = min(close - low, high - close) / (high - low)
# pos_range = (close - low) / (high - low)

print(f"Total 1s long cases: {len(df)}")

# Let's inspect all cases where C_int == 2 vs C_int == 1
print("\nCases with C = 2:")
print(df[df['C_int'] == 2][['id', 'n', 'C_int', 'close', 'range', 'dist_ext', 'n/18.3']])

print("\nCases with C = 1 (near transition, n >= 30):")
print(df[(df['C_int'] == 1) & (df['n'] >= 30)][['id', 'n', 'C_int', 'close', 'range', 'dist_ext', 'n/18.3']])

# Let's test a Failure Swing / Extreme Proximity threshold model:
# For n >= 37: x >= 2.02, C is naturally 2 (or floor(x) = 2).
# For n in [33..36]:
#   If price is at the extreme / breakout level (dist_ext <= threshold): C = 2
#   If price is pulling back / failure swing (dist_ext > threshold): C = 1
# Let's sweep threshold from 0.01 to 0.20 to see if an exact separation exists:

results = []
for th in np.linspace(0.01, 0.20, 39):
    # Model:
    # If n >= 36: C = 2
    # If n == 33: C = 2 if dist_ext <= th else 1
    # Else: floor(n / 18.3)
    preds = []
    for idx, r in df.iterrows():
        n = r['n']
        d_ext = r['dist_ext']
        x = n / 18.3
        
        # Hypothesis:
        # State 2 triggers if x >= 2.0 OR (x >= 1.80 and d_ext <= th)
        # Note: at n=36, x = 1.967, d_ext = 0.1807
        # at n=33, x = 1.803, d_ext = 0.0301 (when C=2) and 0.1265 (when C=1)
        # at n=34, x = 1.858, d_ext = 0.1265 (C=1)
        # at n=35, x = 1.913, d_ext = 0.1145 (C=1)
        
        # Let's test:
        # Effective n: n_eff = n + bonus_ext
        # where bonus_ext depends on proximity to extreme
        pass

# Let's analyze the exact separation between n=33 (C=2 vs C=1):
# At n=33 (140400_n33): dist_ext = 0.0301, C = 2
# At n=33 (140401_n33): dist_ext = 0.1265, C = 1
# At n=34 (140400_n34): dist_ext = 0.1265, C = 1
# At n=35 (140400_n35): dist_ext = 0.1145, C = 1
# At n=36 (140400_n36): dist_ext = 0.1807, C = 2
# At n=37..40: x > 2.0, C = 2

print("\nExact separation boundaries:")
print(f"Max dist_ext for C=2 at n=33: 0.0301")
print(f"Min dist_ext for C=1 at n=33..35: 0.1145")
print(f"Clear margin of separation: [0.0301, 0.1145] -> Midpoint: ~0.072 (7.2% of range)")
