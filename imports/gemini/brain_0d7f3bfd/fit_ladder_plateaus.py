import numpy as np
import pandas as pd

# The confirmed clean baseline plateaus:
plateaus = [
    {'name': 'Ep14_wide_down', 'rng': 107.25, 'atr': 19.85, 'c': 62.0},
    {'name': 'Ep15_wide_up',   'rng': 87.75,  'atr': 11.20, 'c': 68.0},
    {'name': 'Ep06_mid_down',  'rng': 49.25,  'atr': 8.35,  'c': 77.0},
    {'name': 'Ep07_mid_lat',   'rng': 37.50,  'atr': 10.50, 'c': 78.0},
    {'name': 'Oct13_fresh',    'rng': 34.88,  'atr': 10.49, 'c': 84.0},
    {'name': 'Oct13_1900',     'rng': 35.00,  'atr': 7.55,  'c': 81.0},
    {'name': 'Ep02_tight',     'rng': 24.00,  'atr': 6.61,  'c': 75.0},
    {'name': 'Ep19_root',      'rng': 24.50,  'atr': 6.20,  'c': 77.0},
    {'name': 'Ep19_breakout',  'rng': 23.50,  'atr': 5.50,  'c': 71.0},
]

df = pd.DataFrame(plateaus)
print(df)

# Let's inspect simple relationships:
# Does C relate to 60 * factor?
# For Delta = 60s, C/60 is lambda:
df['lambda'] = df['c'] / 60.0
df['k_rung'] = np.round((df['lambda'] - 1.0) / 0.05)
df['c_from_rung'] = 60.0 + df['k_rung'] * 3.0
df['diff'] = df['c'] - df['c_from_rung']
print("\nQuantization ladder fit:")
print(df[['name', 'rng', 'c', 'lambda', 'k_rung', 'c_from_rung', 'diff']])
