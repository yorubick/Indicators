import pandas as pd
import numpy as np
import tabulate_1s_structural_features as t1s

df = t1s.df[t1s.df['n'] >= 21].copy()

# Test smooth continuous ramp:
# delta_FS(dist_ext) = A * max(0, 1 - dist_ext / D_max)
# For dist_ext = 0.0301 (n=33, C=2):
# We need n/18 + delta_FS >= 2.0 -> 1.8333 + delta_FS >= 2.0 -> delta_FS >= 0.1667.
# For dist_ext = 0.0723 (n=32, C=1):
# We need n/18 + delta_FS < 2.0 -> 1.7778 + delta_FS < 2.0 -> delta_FS < 0.2222.
# For dist_ext = 0.1145 (n=35, C=1):
# We need 35/18 + delta_FS < 2.0 -> 1.9444 + delta_FS < 2.0 -> delta_FS < 0.0556.

# Let D_max = 0.08 (8% of range), A = 0.25:
# At d = 0.0301: delta_FS = 0.25 * (1 - 0.0301/0.08) = 0.25 * 0.62375 = 0.1559 -> 1.8333 + 0.1559 = 1.989 (just below 2.0).
# What if A = 0.28, D_max = 0.07?
# At d = 0.0301: delta_FS = 0.28 * (1 - 0.0301/0.07) = 0.28 * 0.57 = 0.1596 -> 1.8333 + 0.1596 = 1.993.
# What if A = 0.35, D_max = 0.06?
# At d = 0.0301: delta_FS = 0.35 * (1 - 0.0301/0.06) = 0.35 * 0.498 = 0.1744 -> 1.8333 + 0.1744 = 2.007 -> floor = 2!
# At d = 0.0723: delta_FS = 0 -> 1.7778 + 0 = 1.7778 -> floor = 1!
# At d >= 0.11: delta_FS = 0 -> floor = 1!

preds_smooth = []
for _, r in df.iterrows():
    n = r['n']
    d = r['dist_ext']
    x = n / 18.0
    # Continuous ramp:
    delta_fs = 0.35 * max(0.0, 1.0 - d / 0.06)
    preds_smooth.append(int(np.floor(x + delta_fs)))

df['pred_smooth'] = preds_smooth
df['match_smooth'] = df['pred_smooth'] == df['C_int']

print(f"Smooth Ramp Model Accuracy: {df['match_smooth'].sum()} / {len(df)} ({df['match_smooth'].mean()*100:.1f}%)")

# Let's inspect all 26 cases with the smooth model:
print(df[['id', 'n', 'C_int', 'pred_smooth', 'match_smooth', 'dist_ext', 'n/18.3']].to_string(index=False))
