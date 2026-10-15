import pandas as pd
import numpy as np
import tabulate_1s_structural_features as t1s

df = t1s.df[t1s.df['n'] >= 21].copy()

# Compare:
# Model A: C = floor(n / 18.0 + (0.2 if dist_ext < 0.05 else 0.0))
# Model B: C = round(n / 18.3) with Failure Swing suppression:
#   At n=28: round(28/18.3) = 2, but actual C = 1.
#   Why was n=28 C=1? In 140400_n28, dist_ext = 0.023, but x = 1.53.
#   In 140200_n28, dist_ext = 0.40, x = 1.53.
#   Both have C = 1!
#   So n=28 is unconditionally 1!
# Model C: Ladder in steps of 18 (or 9 bars):
#   n = 21..35: C = 1 (except active extreme impulse at n=33 gives 2)
#   n >= 36: C = 2

preds_A = []
for _, r in df.iterrows():
    n = r['n']
    d = r['dist_ext']
    x = n / 18.0
    boost = 0.20 if d < 0.05 else 0.0
    preds_A.append(int(np.floor(x + boost)))

df['pred_A'] = preds_A
df['match_A'] = df['pred_A'] == df['C_int']

print(f"Model A Accuracy: {df['match_A'].sum()} / {len(df)} ({df['match_A'].mean()*100:.1f}%)")

print("\nFull comparison table for Model A:")
print(df[['id', 'n', 'C_int', 'pred_A', 'match_A', 'dist_ext', 'pos_range', 'n/18.3']].to_string(index=False))
