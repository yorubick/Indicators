import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

# Load 13 Oct series as well
with open(r'G:\trading\guias\analisis\C_evolucion87_resultados.json') as f:
    data13 = json.load(f)

# Combine training long cases (32 cases) + 13 Oct series (6 cases)
train_cases = [c for c in data['cases'] if c['branch'] == 'long' and c['split'] == 'training']
oct13_cases = []
for c in data13['cases']:
    oct13_cases.append({
        'id': f"oct13_{c['END'][11:16]}",
        'START': '2026-10-13T06:25:00+00:00',
        'END': c['END'],
        'bars': c['bars'],
        'dt': 60,
        'C': c['C'],
        'split': 'training_oct13',
        'OHLC': data13['cases'][0]['END_OHLC'] # not full, but we have range
    })

print(f"Total training cases: {len(train_cases)}, Oct 13 cases: {len(oct13_cases)}")

# Let's test the discriminator on Episode 19 cases:
ep19 = [c for c in train_cases if c['START'].startswith('2026-10-12T19:0')]

print("\n=== EPISODE 19: DISCRIMINATING 19:00-19:01 FROM 19:02-19:04 ===")
for c in sorted(ep19, key=lambda x: (x['START'], x['bars'])):
    ohlc = c['OHLC']
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    opens = [x['open'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    
    rng = max(highs) - min(lows)
    start_pos = (opens[0] - min(lows)) / rng if rng > 0 else 0.5
    end_pos = (closes[-1] - min(lows)) / rng if rng > 0 else 0.5
    first_rng = highs[0] - lows[0]
    
    # ATR of range
    trs = [highs[0]-lows[0]] + [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, len(closes))]
    atr = np.mean(trs)
    
    n = c['bars']
    dt = c['dt']
    t_span = (n - 1) * dt
    C = round(c['C'])
    
    # Check if end bar is new high
    is_new_high = highs[-1] > max(highs[:-1])
    
    # Proposed Discriminator:
    # If start_pos > 0.35 and not is_new_high: Consolidation -> C = floor(t_span / 24)
    # If is_new_high: Breakout -> C = 71
    # Else: Macro Base -> C = 77
    if is_new_high and rng <= 26.0:
        pred_C = 71
        state = "BREAKOUT"
    elif start_pos > 0.35 and not is_new_high and n <= 25:
        pred_C = int(np.floor(t_span / 24))
        state = "CONSOLIDATION"
    elif c['dt'] == 15:
        pred_C = 16
        state = "15S_SPECIAL"
    else:
        pred_C = 77
        state = "BASE_77"
        
    match = (pred_C == C)
    err = pred_C - C
    print(f"[{state:13s}] {c['START'][11:16]}->{c['END'][11:16]} n={n:2d} | start_pos={start_pos:.2f} | Actual={C:3d} Pred={pred_C:3d} | Match={match} (err={err:+3d})")
