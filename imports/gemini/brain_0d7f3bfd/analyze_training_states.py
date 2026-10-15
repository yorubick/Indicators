import json
import numpy as np

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

train_cases = [c for c in data['cases'] if c['branch'] == 'long' and c['split'] == 'training' and c['dt'] == 60]

print(f"Total long training cases with dt=60: {len(train_cases)}")

# Group by the observed C values
c_groups = {}
for c in train_cases:
    c_val = round(c['C'])
    c_groups.setdefault(c_val, []).append(c)

print("\nDistribution of C in Training:")
for c_val, group in sorted(c_groups.items()):
    print(f"C = {c_val:3d} ({len(group)} cases): {[g['START'][11:16]+'->'+g['END'][11:16]+'(n='+str(g['bars'])+')' for g in group]}")

# Let's inspect features for each group:
print("\nGroup Feature Summary:")
print("C   | Count | Range (pts) | Close-to-High dist | High-to-End bars | New High at END?")
print("-" * 80)
for c_val, group in sorted(c_groups.items()):
    ranges = []
    dist_highs = []
    bars_from_high = []
    new_highs = []
    for g in group:
        ohlc = g['OHLC']
        highs = [x['high'] for x in ohlc]
        lows = [x['low'] for x in ohlc]
        closes = [x['close'] for x in ohlc]
        rng = max(highs) - min(lows)
        ranges.append(rng)
        
        # distance from close to global high
        h_max = max(highs)
        dist_h = h_max - closes[-1]
        dist_highs.append(dist_h)
        
        # bars from global high to end
        imax = highs.index(h_max)
        bars_from_high.append(len(highs) - 1 - imax)
        
        # was end bar a new high?
        prev_max = max(highs[:-1])
        new_highs.append(highs[-1] > prev_max)
        
    print(f"{c_val:3d} | {len(group):5d} | {np.mean(ranges):5.2f} pts  | {np.mean(dist_highs):6.2f} pts       | {np.mean(bars_from_high):4.1f} bars        | {sum(new_highs)}/{len(group)} new H")
