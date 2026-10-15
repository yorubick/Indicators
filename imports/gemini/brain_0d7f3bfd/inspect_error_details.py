import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

# Inspect all cases with error > 3s from evaluate_unified_model_v2
import evaluate_unified_model_v2 as ev
df = ev.df

err_cases = df[df['abs_err'] > 3.0].to_dict('records')

print(f"Total error cases > 3s: {len(err_cases)}\n")

for ec in err_cases:
    cid = ec['id']
    # find raw case
    raw = None
    for c in data['cases']:
        if c['id'] == cid:
            raw = c
            break
    if not raw:
        continue
    ohlc = raw['OHLC']
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    opens = [x['open'] for x in ohlc]
    closes = [x['close'] for x in ohlc]
    rng = max(highs) - min(lows)
    sp = (opens[0] - min(lows)) / rng if rng > 0 else 0.5
    
    # Analyze the last candle
    last_o = opens[-1]
    last_h = highs[-1]
    last_l = lows[-1]
    last_c = closes[-1]
    prev_c = closes[-2] if len(closes) > 1 else last_o
    last_body = last_c - last_o
    last_range = last_h - last_l
    
    # Peak / trough positions
    arg_max = np.argmax(highs)
    arg_min = np.argmin(lows)
    dist_from_max = len(highs) - 1 - arg_max
    dist_from_min = len(lows) - 1 - arg_min
    
    print(f"ID: {cid} | Split: {ec['split']} | Bars: {ec['bars']} | Act C: {ec['actual']} | Pred: {ec['pred']} | Err: {ec['error']:+.1f}")
    print(f"   Rng: {rng:.2f} | StartPos: {sp:.2f} | DistMax: {dist_from_max} | DistMin: {dist_from_min}")
    print(f"   Last candle: O={last_o}, H={last_h}, L={last_l}, C={last_c}, Body={last_body:+.2f}")
    print(f"   MaxHigh: {max(highs)} at bar {arg_max}, MinLow: {min(lows)} at bar {arg_min}")
    print("-" * 75)
