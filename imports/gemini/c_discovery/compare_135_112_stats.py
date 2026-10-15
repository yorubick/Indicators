import pandas as pd
import numpy as np

# Load candles
from deep_inspect_candles import res, df, start_idx

print("Detailed inspection of 19:26 - 19:35:")
print(res[["END", "n", "C", "Open", "High", "Low", "Close", "Vol", "body", "rng", "dist_H"]])

# Check differences between C=135/136 and C=112
c135 = res[res["C"] >= 134]
c112 = res[res["C"] == 112]

print("\n--- C >= 134 bars ---")
print(c135[["END", "n", "C", "Open", "High", "Low", "Close", "Vol", "body", "rng", "dist_H"]])

print("\n--- C == 112 bars ---")
print(c112[["END", "n", "C", "Open", "High", "Low", "Close", "Vol", "body", "rng", "dist_H"]])
