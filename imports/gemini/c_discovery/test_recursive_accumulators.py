import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = {c['id']: c for c in master['cases']}

c88 = cases['20261012_190315_192345_15s']
c61 = cases['20261012_190330_192345_15s']

df88 = pd.DataFrame(c88['OHLCV'])
df61 = pd.DataFrame(c61['OHLCV'])

print("Comparing Recursive Accumulators between C88 and C61:")
print(f"C88 (START 19:03:15, C=88): n = {len(df88)}")
print(f"C61 (START 19:03:30, C=61): n = {len(df61)}")

# In Pine Script, EMA is initialized as:
# ema := na(ema[1]) ? src : alpha * src + (1 - alpha) * ema[1]
# Let's test alpha values: 2/(length + 1) for lengths 3, 9, 13, 20, 21, 27
for length in [3, 9, 13, 20, 21, 27]:
    alpha = 2.0 / (length + 1)
    
    # Volume EMA
    ema_vol_88 = [df88['volume'].iloc[0]]
    for v in df88['volume'].iloc[1:]:
        ema_vol_88.append(alpha * v + (1 - alpha) * ema_vol_88[-1])
        
    ema_vol_61 = [df61['volume'].iloc[0]]
    for v in df61['volume'].iloc[1:]:
        ema_vol_61.append(alpha * v + (1 - alpha) * ema_vol_61[-1])
        
    # Price EMA (close)
    ema_c_88 = [df88['close'].iloc[0]]
    for p in df88['close'].iloc[1:]:
        ema_c_88.append(alpha * p + (1 - alpha) * ema_c_88[-1])
        
    ema_c_61 = [df61['close'].iloc[0]]
    for p in df61['close'].iloc[1:]:
        ema_c_61.append(alpha * p + (1 - alpha) * ema_c_61[-1])
        
    print(f"\nLength {length:2d} (alpha = {alpha:.4f}):")
    print(f"  Vol EMA at END:  88 -> {ema_vol_88[-1]:.3f} | 61 -> {ema_vol_61[-1]:.3f} | diff = {ema_vol_88[-1] - ema_vol_61[-1]:.3f}")
    print(f"  Close EMA at END: 88 -> {ema_c_88[-1]:.3f} | 61 -> {ema_c_61[-1]:.3f} | diff = {ema_c_88[-1] - ema_c_61[-1]:.3f}")
