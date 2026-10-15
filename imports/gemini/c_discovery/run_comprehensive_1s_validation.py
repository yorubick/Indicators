import json
import pandas as pd
import numpy as np
import tabulate_1s_structural_features as t1s

df = t1s.df[t1s.df['n'] >= 21].copy()

def predict_C_1s(row):
    n = row['n']
    d_ext = row['dist_ext']
    x = n / 18.0
    boost = 0.20 if d_ext < 0.05 else 0.0
    return int(np.floor(x + boost))

df['C_pred'] = df.apply(predict_C_1s, axis=1)
df['residual'] = df['C_int'] - df['C_pred']
df['exact_match'] = df['residual'] == 0

print("================================================================================")
print("COMPREHENSIVE VALIDATION REPORT: FAILURE SWING MODULATED OPERATOR (1s DATASET)")
print("================================================================================")
print(f"Total Evaluated Cases: {len(df)}")
print(f"Exact Matches: {df['exact_match'].sum()} / {len(df)} ({df['exact_match'].mean()*100:.1f}%)")
print(f"Max Absolute Residual: {df['residual'].abs().max()}")
print(f"Mean Squared Error: {(df['residual']**2).mean():.6f}")

print("\nDetailed Case Log:")
cols = ['id', 'n', 'C_int', 'C_pred', 'residual', 'exact_match', 'dist_ext', 'pos_range', 'close', 'range']
print(df[cols].to_string(index=False))

# Check Short Regime verification consistency
print("\nShort Regime Verification (n < 21):")
df_short = t1s.df[t1s.df['n'] < 21].copy()
for _, r in df_short.iterrows():
    pred_short = max(1.0, r['n'] * 1.0 * 10.0 / 183.0)
    res = abs(r['C'] - pred_short)
    print(f"id: {r['id']}, n: {r['n']}, C_real: {r['C']:.10f}, C_pred: {pred_short:.10f}, res: {res:.2e}")
