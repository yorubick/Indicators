import json
import numpy as np

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

cases = data['cases']
long_cases = [c for c in cases if c['bars'] >= 21]

print(f"Total long cases: {len(long_cases)}")

# Group by episode/regime
# We can identify episodes by date and hour of START
episodes = {}
for c in long_cases:
    dt = c['dt']
    start = c['START']
    end = c['END']
    bars = c['bars']
    C = round(c['C'])
    split = c['split']
    
    # Calculate price metrics
    ohlc = c['OHLC']
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    opens = [x['open'] for x in ohlc]
    
    rng = max(highs) - min(lows)
    net_disp = closes[-1] - opens[0]
    total_path = sum(abs(closes[i] - closes[i-1]) for i in range(1, len(closes)))
    
    ep_key = start[:13] # e.g. '2026-10-12T06'
    episodes.setdefault(ep_key, []).append({
        'id': c['id'],
        'START': start,
        'END': end,
        'bars': bars,
        'dt': dt,
        'C': C,
        'C_raw': c['C'],
        'split': split,
        'range': rng,
        'net_disp': net_disp,
        'total_path': total_path,
        'high': max(highs),
        'low': min(lows),
        'open0': opens[0],
        'closeN': closes[-1]
    })

for ep, items in sorted(episodes.items()):
    print(f"\n================ EPISODE {ep} ({len(items)} cases) ================")
    for it in sorted(items, key=lambda x: (x['START'], x['bars'])):
        print(f"[{it['split']:10s}] {it['START'][11:19]}->{it['END'][11:19]} | bars={it['bars']:2d} dt={it['dt']:3d} | C={it['C']:3d} | Rng={it['range']:6.2f} Net={it['net_disp']:6.2f} Path={it['total_path']:6.2f}")
