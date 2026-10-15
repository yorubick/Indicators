import json
import pandas as pd
import numpy as np

# Load df from previous step
# Let's run comparison on all 28 1s cases
import tabulate_1s_structural_features as t1s

df = t1s.df.copy()
# Filter long cases n >= 21
df_long = df[df['n'] >= 21].copy()

df_long['floor_pred'] = np.floor(df_long['n'] / 18.3).astype(int)
df_long['round_pred'] = np.round(df_long['n'] / 18.3).astype(int)

df_long['floor_match'] = df_long['floor_pred'] == df_long['C_int']
df_long['round_match'] = df_long['round_pred'] == df_long['C_int']

print("1-Second Long Regime (n >= 21) Evaluation (N = %d):" % len(df_long))
print(f"Floor match count: {df_long['floor_match'].sum()} / {len(df_long)} ({df_long['floor_match'].mean()*100:.1f}%)")
print(f"Round match count: {df_long['round_match'].sum()} / {len(df_long)} ({df_long['round_match'].mean()*100:.1f}%)")

print("\nMismatches for Floor:")
print(df_long[~df_long['floor_match']][['id', 'n', 'C_int', 'floor_pred', 'round_pred', 'pos_range', 'dist_ext', 'n/18.3']])

print("\nMismatches for Round:")
print(df_long[~df_long['round_match']][['id', 'n', 'C_int', 'floor_pred', 'round_pred', 'pos_range', 'dist_ext', 'n/18.3']])
