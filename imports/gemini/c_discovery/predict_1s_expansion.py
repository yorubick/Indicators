import numpy as np
import pandas as pd

# Let's compute the thresholds where various models predict C abandons 1.0 on a 1s chart:

print("="*70)
print("PREDICTIONS FOR 1-SECOND CHART EXPANSION (n >= 21, dt = 1s)")
print("="*70)

# Model 1: Continuous short formula rounded: round(n * 10 / 183)
# round(n * 10 / 183) >= 1.5 => n >= 1.5 * 18.3 = 27.45 => n = 28
# Model 2: Floor: floor(n * 10 / 183) >= 2 => n >= 2 * 18.3 = 36.6 => n = 37
# Model 3: Fibonacci / Power of 3 cycle:
# Cycle length = 27 bars (half-cycle is 13 or 14 bars, full rung is 27 or 81 bars)
# If C jumps on power-of-3 rungs: 1s -> 3s at n = 27 or n = 55 (Fibonacci) or n = 81 (3^4)

rows = []
for n in range(20, 90):
    val_cont = n * 10.0 / 183.0
    val_round = round(val_cont)
    val_floor = int(np.floor(val_cont))
    val_ceil = int(np.ceil(val_cont))
    
    rows.append({
        'n': n,
        'val_cont': round(val_cont, 4),
        'round_18_3': val_round,
        'floor_18_3': val_floor,
    })

df = pd.DataFrame(rows)
print("Key transition points in continuous rounding:")
print(df[df['n'].isin([20, 21, 22, 26, 27, 28, 29, 36, 37, 54, 55, 81, 82])].to_string(index=False))

print("\nCritical Transition Boundaries to Test:")
print("1. n = 27 -> n = 28: If C = round(n/18.3), C stays 1 up to n=27, then becomes 2 at n=28.")
print("2. n = 27 (Power of 3 / cycle): Does it jump to 3s (ladder step)?")
print("3. n = 36 -> n = 37: If C = floor(n/18.3), C stays 1 up to n=36, then becomes 2 at n=37.")
print("4. n = 55 (Fibonacci): 55 * 10 / 183 = 3.0055 -> exactly 3.0!")
