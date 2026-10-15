import pandas as pd
from feature_table_long import feat_df

feat_df['n_eff'] = feat_df['C'] * 183.0 / (10.0 * feat_df['dt'])
feat_df['n_eff_round'] = feat_df['n_eff'].round()
feat_df['n_diff'] = feat_df['n'] - feat_df['n_eff']

print("Summary of n_eff:")
print(feat_df[['dt', 'n', 'C', 'n_eff', 'n_eff_round', 'n_diff']].describe())

print("\nSample cases where n=21 on 60s chart:")
sample_21 = feat_df[(feat_df['dt']==60) & (feat_df['n']==21)][['id', 'C', 'n_eff', 'n_eff_round', 'n_diff']]
print(sample_21.to_string())
