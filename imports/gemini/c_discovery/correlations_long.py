import json
import numpy as np
import pandas as pd
from scipy import stats

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

cases = [c for c in master["cases"] if c.get("bars") >= 21 and c.get("C_Lite") is not None]

print(f"Total long cases with C_Lite: {len(cases)}")

data = []
for c in cases:
    ohlcv = c["OHLCV"]
    df = pd.DataFrame(ohlcv)
    dt = c["dt"]
    n = c["bars"]
    C = c["C_Lite"]
    
    # Calculate basic metrics
    high = df['high'].max()
    low = df['low'].min()
    rng = high - low
    
    close_start = df.iloc[0]['close']
    close_end = df.iloc[-1]['close']
    net_chg = abs(close_end - close_start)
    
    # Path length / total variation
    path_len = np.sum(np.abs(np.diff(df['close'])))
    er = net_chg / path_len if path_len > 0 else 0
    
    # True range
    tr = np.maximum(df['high'].iloc[1:].values - df['low'].iloc[1:].values,
                    np.maximum(np.abs(df['high'].iloc[1:].values - df['close'].iloc[:-1].values),
                               np.abs(df['low'].iloc[1:].values - df['close'].iloc[:-1].values)))
    atr = np.mean(tr) if len(tr) > 0 else rng
    
    # Standard deviation
    std_close = df['close'].std()
    
    # Volume metrics
    vol_sum = df['volume'].sum() if 'volume' in df and not df['volume'].isna().all() else 0
    vol_mean = df['volume'].mean() if 'volume' in df and not df['volume'].isna().all() else 0
    
    # Duration
    duration = (n - 1) * dt
    
    data.append({
        'id': c['id'],
        'dt': dt,
        'n': n,
        'duration': duration,
        'C': C,
        'C_over_dt': C / dt,
        'C_over_dur': C / duration,
        'rng': rng,
        'net_chg': net_chg,
        'path_len': path_len,
        'er': er,
        'atr': atr,
        'std_close': std_close,
        'vol_sum': vol_sum,
        'vol_mean': vol_mean
    })

res = pd.DataFrame(data)

# Let's check correlations with C
print("\n--- Pearson correlations with C ---")
for col in ['dt', 'n', 'duration', 'rng', 'net_chg', 'path_len', 'er', 'atr', 'std_close', 'vol_sum']:
    r, p = stats.pearsonr(res[col], res['C'])
    sr, sp = stats.spearmanr(res[col], res['C'])
    print(f"{col:12s}: Pearson = {r:7.4f} (p={p:.2e}), Spearman = {sr:7.4f} (p={sp:.2e})")

# Separate by dt
for dt_val in sorted(res['dt'].unique()):
    sub = res[res['dt'] == dt_val]
    print(f"\n--- Correlations for dt = {dt_val} (count = {len(sub)}) ---")
    for col in ['n', 'duration', 'rng', 'net_chg', 'path_len', 'er', 'atr', 'std_close', 'vol_sum']:
        r, _ = stats.pearsonr(sub[col], sub['C'])
        sr, _ = stats.spearmanr(sub[col], sub['C'])
        print(f"  {col:12s}: Pearson = {r:7.4f}, Spearman = {sr:7.4f}")
