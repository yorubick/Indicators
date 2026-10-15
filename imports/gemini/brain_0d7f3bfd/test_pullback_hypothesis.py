import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

long_cases = [c for c in data['cases'] if c['bars'] >= 21 and c['dt'] == 60]

print(f"Total long 60s cases: {len(long_cases)}")

rows = []
for c in long_cases:
    ohlc = c['OHLC']
    n = c['bars']
    C = round(c['C'])
    split = c['split']
    
    opens = np.array([x['open'] for x in ohlc])
    highs = np.array([x['high'] for x in ohlc])
    lows = np.array([x['low'] for x in ohlc])
    closes = np.array([x['close'] for x in ohlc])
    
    net_move = closes[-1] - opens[0]
    trend_dir = "BULL" if net_move > 0 else "BEAR"
    
    # End candle direction
    end_candle_dir = "UP" if closes[-1] >= opens[-1] else "DN"
    
    # Is end candle a pullback?
    # If BULL trend and end candle is DN -> Pullback!
    # If BEAR trend and end candle is UP -> Pullback!
    is_pullback = (trend_dir == "BULL" and end_candle_dir == "DN") or (trend_dir == "BEAR" and end_candle_dir == "UP")
    
    # Did end candle make a new extreme?
    prev_max = np.max(highs[:-1])
    prev_min = np.min(lows[:-1])
    is_new_high = highs[-1] > prev_max
    is_new_low = lows[-1] < prev_min
    is_expansion = is_new_high or is_new_low
    
    rows.append({
        'id': c['id'][:25],
        'split': split,
        'START': c['START'][11:16],
        'END': c['END'][11:16],
        'n': n,
        'C': C,
        'trend': trend_dir,
        'end_dir': end_candle_dir,
        'is_pullback': is_pullback,
        'is_expansion': is_expansion,
        'net': round(net_move, 2)
    })

df = pd.DataFrame(rows)

print("\n--- PULLBACK VS EXPANSION COMPARISON ---")
print("Pullback cases (End candle against trend):")
print(df[df['is_pullback']].to_string())

print("\nExpansion cases (End candle makes new extreme):")
print(df[df['is_expansion']].to_string())

print("\nSummary of C by type:")
print("Pullback C mean:", df[df['is_pullback']]['C'].mean(), "median:", df[df['is_pullback']]['C'].median(), "values:", sorted(list(df[df['is_pullback']]['C'])))
print("Expansion C mean:", df[df['is_expansion']]['C'].mean(), "median:", df[df['is_expansion']]['C'].median(), "values:", sorted(list(df[df['is_expansion']]['C'])))
