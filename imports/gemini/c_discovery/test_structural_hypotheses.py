import json
import pandas as pd
import numpy as np

# Load the 1s cases
with open(r'C:\Users\PC\.gemini\antigravity\scratch\c_discovery\tabulate_1s_structural_features.py', 'r') as f:
    pass

# We will create an analysis script to systematically test hypothesis for the 1s transition
# Candidates:
# 1. Effective n: n_eff = n - bars_since_extreme, or n_eff = f(range, close, open)
# 2. Threshold hysteresis / failure swing:
#    If price is near extreme (dist_ext < threshold) vs consolidating
# 3. Ratio of (Close - Open_0) or (Close - midpoint)
# 4. Box extension levels (Fibonacci / standard deviations):
#    Did the bar touch a specific projection level?
