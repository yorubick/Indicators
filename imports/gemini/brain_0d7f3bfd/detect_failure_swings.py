import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

# Let's inspect the failure swing detection across all long cases:
# Conditions for a Bearish Failure Swing (after an uptrend/high):
# 1. high[1] was highest high so far: high[1] == max(highs)
# 2. current bar high < high[1] (failed to make higher high)
# 3. current bar close < open or close < low[1]
#
# Conditions for a Bullish Failure Swing (after a downtrend/low):
# 1. low[1] was lowest low so far: low[1] == min(lows)
# 2. current bar low > low[1] (failed to make lower low)
# 3. current bar close > open or close > high[1]

for c in data['cases']:
    if c['bars'] >= 21 and c['dt'] == 60:
        ohlc = c['OHLC']
        highs = [x['high'] for x in ohlc]
        lows = [x['low'] for x in ohlc]
        opens = [x['open'] for x in ohlc]
        closes = [x['close'] for x in ohlc]
        n = len(ohlc)
        
        # Check if last bar is a failure swing bar:
        prev_is_max = (highs[-2] == max(highs))
        curr_failed_h = (highs[-1] < highs[-2])
        is_bear_sfp = prev_is_max and curr_failed_h
        
        prev_is_min = (lows[-2] == min(lows))
        curr_failed_l = (lows[-1] > lows[-2])
        is_bull_sfp = prev_is_min and curr_failed_l
        
        # Distance of extreme from END:
        arg_max = np.argmax(highs)
        arg_min = np.argmin(lows)
        dist_max = n - 1 - arg_max
        dist_min = n - 1 - arg_min
        
        act_c = round(c['C'])
        
        if is_bear_sfp or is_bull_sfp or dist_max == 1 or dist_min == 1:
            print(f"SFP candidate: {c['id'][:26]} | bars={n} | C={act_c} | BearSFP={is_bear_sfp} | BullSFP={is_bull_sfp} | DistMax={dist_max} | DistMin={dist_min}")
