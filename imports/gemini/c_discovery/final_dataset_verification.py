import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = master['cases']

short_lite = [c for c in cases if c['bars'] < 21 and c.get('C_Lite') is not None]
long_lite = [c for c in cases if c['bars'] >= 21 and c.get('C_Lite') is not None]
char_only = [c for c in cases if c.get('C_Lite') is None]

print(f"Total cases: {len(cases)}")
print(f"Short Lite cases (n < 21): {len(short_lite)}")
print(f"Long Lite cases (n >= 21): {len(long_lite)}")
print(f"Character-only cases: {len(char_only)}")

# Check short residuals
short_residuals = []
for c in short_lite:
    pred = max(c['dt'], c['bars'] * c['dt'] * 10.0 / 183.0)
    short_residuals.append(abs(c['C_Lite'] - pred))

print(f"Short regime max residual: {max(short_residuals):.2e}")

# Check long integer residuals
long_int_residuals = []
for c in long_lite:
    long_int_residuals.append(abs(c['C_Lite'] - round(c['C_Lite'])))

print(f"Long regime max integer residual: {max(long_int_residuals):.2e}")

# Check Character intervals
char_int_valid = 0
for c in char_only:
    low = c['C_Character_interval']['lower_inclusive']
    high = c['C_Character_interval']['upper_exclusive']
    ints = [i for i in range(int(np.floor(low)), int(np.ceil(high)) + 1) if low <= i < high]
    if len(ints) == 1:
        char_int_valid += 1

print(f"Character intervals with exactly 1 integer: {char_int_valid} / {len(char_only)}")
