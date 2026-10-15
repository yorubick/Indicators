import pandas as pd
import numpy as np
from test_operator_candidates import res_df, df, idx_start

print("=== ANALYSIS OF GROUND TRUTH 19:03 (n=21..32) ===")
print(res_df[["END", "n", "C", "N", "bar_rng", "body", "close_loc", "new_H", "close_above_prev_H", "dist_to_H", "er", "slope_3"]])

# Let's inspect differences between N=54 and N=45
df_54 = res_df[res_df["N"] == 54]
df_45 = res_df[res_df["N"] == 45]

print("\n--- Summary for N = 54 (C = 135/136) ---")
print(df_54[["END", "n", "bar_rng", "body", "close_loc", "new_H", "close_above_prev_H", "dist_to_H", "er", "slope_3"]])

print("\n--- Summary for N = 45 (C = 112) ---")
print(df_45[["END", "n", "bar_rng", "body", "close_loc", "new_H", "close_above_prev_H", "dist_to_H", "er", "slope_3"]])
