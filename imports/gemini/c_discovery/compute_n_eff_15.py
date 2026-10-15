import pandas as pd
from feature_table_long import feat_df

feat_df['n_eff'] = feat_df['C'] * 183.0 / (10.0 * feat_df['dt'])
feat_df['n_eff_round'] = feat_df['n_eff'].round()
feat_df['n_diff'] = feat_df['n'] - feat_df['n_eff']

sample_15 = feat_df[feat_df['dt']==15][['id', 'n', 'C', 'n_eff', 'n_eff_round', 'n_diff']]
print("Sample 15s cases:")
print(sample_15.to_string())
