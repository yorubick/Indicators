import pandas as pd
from feature_table_long import feat_df

feat_df['pred_short'] = feat_df['total_sec'] * 10.0 / 183.0
feat_df['diff'] = feat_df['C'] - feat_df['pred_short']
feat_df['ratio_c_pred'] = feat_df['C'] / feat_df['pred_short']

corrs_diff = feat_df.corr(numeric_only=True)['diff'].sort_values(ascending=False)
print("Correlations with diff (C - pred_short):")
print(corrs_diff)

print("\nCorrelations with ratio (C / pred_short):")
corrs_ratio = feat_df.corr(numeric_only=True)['ratio_c_pred'].sort_values(ascending=False)
print(corrs_ratio)
