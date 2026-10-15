import evaluate_unified_model_v3 as ev

df = ev.df
err3 = df[df['abs_err'] > 3.0].sort_values(by='abs_err', ascending=False)
print("REMAINING CASES WITH abs_err > 3s (Total:", len(err3), "):")
print(err3[['id', 'split', 'bars', 'dt', 'actual', 'pred', 'error', 'branch_model']].to_string())
