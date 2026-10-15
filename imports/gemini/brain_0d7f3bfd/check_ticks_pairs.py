from master_cases import dataset
import numpy as np

print("Testing if C corresponds to the number of ticks between two price levels:")

for d in dataset[:25]:
    sub = d['sub']
    dt = d['dt']
    C = d['C']
    target_pts = C * 0.25  # C ticks
    
    # Collect all key price levels:
    # Highs, Lows, Opens, Closes of all candles
    highs = [x['high'] for x in sub]
    lows = [x['low'] for x in sub]
    opens = [x['open'] for x in sub]
    closes = [x['close'] for x in sub]
    
    # Check max_h - min_l
    max_h = max(highs)
    min_l = min(lows)
    range_pts = max_h - min_l
    range_ticks = range_pts / 0.25
    
    # Check if target_pts exists between any high and low, or open and close
    # Find all pairs of (price1, price2) where abs(price1 - price2) == target_pts
    prices = set(highs + lows + opens + closes)
    pairs = []
    for p1 in prices:
        p2 = p1 - target_pts
        if p2 in prices:
            pairs.append((p1, p2))
            
    print(f"{d['s']:8s} {d['e']:8s} {dt:2d}s | C={C:3d} (target={target_pts:5.2f} pts) | Range={range_pts:5.2f} ({range_ticks:3.0f} tks) | Matching pairs: {len(pairs)}")
    if pairs and len(pairs) <= 3:
        for p1, p2 in pairs:
            print(f"      Pair: {p1:.2f} - {p2:.2f} = {p1-p2:.2f}")
