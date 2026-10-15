import numpy as np
import pandas as pd

resting_states = [
    {'name': 'Ep 14 (14:00)', 'rng': 107.25, 'atr': 19.76, 'C': 62},
    {'name': 'Ep 15 (15:30)', 'rng': 87.75,  'atr': 11.23, 'C': 68},
    {'name': 'Ep 06 (06:00)', 'rng': 49.25,  'atr': 8.36,  'C': 77},
    {'name': 'Ep 07 (07:00)', 'rng': 37.50,  'atr': 10.67, 'C': 75},
    {'name': 'Ep 13-19:00',   'rng': 35.00,  'atr': 7.55,  'C': 81},
    {'name': 'Ep 13-06:25',   'rng': 30.75,  'atr': 8.00,  'C': 84},
    {'name': 'Ep 19-19:00',   'rng': 24.50,  'atr': 6.30,  'C': 77},
    {'name': 'Ep 04 (04:45)', 'rng': 24.00,  'atr': 6.61,  'C': 75},
]

df = pd.DataFrame(resting_states).sort_values('rng', ascending=False)
print("=== RESTING STATE C VS RANGE ===")
print(df.to_string())

# Linear fit of C vs Range
slope, intercept = np.polyfit(df['rng'], df['C'], 1)
print(f"\nLinear Fit: C = {intercept:.2f} + ({slope:.3f}) * Range")
print(f"Correlation: {df['rng'].corr(df['C']):.3f}")

# What if we fit C vs 1 / sqrt(Range) or log(Range)?
for name, x in [('Range', df['rng']), ('1/Range', 1/df['rng']), ('sqrt(Range)', np.sqrt(df['rng'])), ('ATR', df['atr']), ('Range/ATR', df['rng']/df['atr'])]:
    corr = x.corr(df['C'])
    print(f"Correlation with {name:10s}: {corr:+.3f}")
