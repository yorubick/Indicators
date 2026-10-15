import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = master['cases']
long_cases = [c for c in cases if c['bars'] >= 21 and c.get('C_Lite') is not None]

print(f"Total long cases to test: {len(long_cases)}")

def find_pivots(df, left, right):
    highs = []
    lows = []
    n = len(df)
    for i in range(left, n - right):
        # High pivot
        if all(df['high'].iloc[i] > df['high'].iloc[i-k] for k in range(1, left+1)) and \
           all(df['high'].iloc[i] >= df['high'].iloc[i+k] for k in range(1, right+1)):
            highs.append(i)
        # Low pivot
        if all(df['low'].iloc[i] < df['low'].iloc[i-k] for k in range(1, left+1)) and \
           all(df['low'].iloc[i] <= df['low'].iloc[i+k] for k in range(1, right+1)):
            lows.append(i)
    return highs, lows

# Let's test across all long cases:
# For each pivot candidate, check if round(duration / 18.3) == C or if abs(duration / 18.3 - C) < 1.0
results_exact = {}
pivot_configs = [(1, 1), (1, 2), (2, 1), (2, 2), (3, 3)]

for left, right in pivot_configs:
    exact_matches_any_pivot = 0
    exact_matches_first_pivot = 0
    exact_matches_last_pivot = 0
    exact_matches_max_pivot = 0
    
    match_details = []
    
    for c in long_cases:
        df = pd.DataFrame(c['OHLCV'])
        dt = c['dt']
        n = len(df)
        c_target = round(c['C_Lite'])
        
        high_pivs, low_pivs = find_pivots(df, left, right)
        all_pivs = sorted(list(set(high_pivs + low_pivs)))
        
        # Test candidate durations from each pivot to END
        matched = False
        candidates = []
        for p in all_pivs:
            # Sub-durations
            dur_bars_incl = n - p
            dur_bars_excl = n - 1 - p
            
            for dur_bars in [dur_bars_incl, dur_bars_excl]:
                dur_sec = dur_bars * dt
                pred = round(dur_sec * 10.0 / 183.0)
                candidates.append((p, dur_bars, dur_sec, pred))
                if pred == c_target:
                    matched = True
        
        if matched:
            exact_matches_any_pivot += 1
            
    print(f"Config ({left}, {right}): {exact_matches_any_pivot} / {len(long_cases)} cases have AT LEAST ONE pivot with round(dur / 18.3) == C")
