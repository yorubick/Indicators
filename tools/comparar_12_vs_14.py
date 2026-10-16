import json
import pandas as pd
import numpy as np

d12 = json.load(open('data/ohlcv_2m_1430_1516.json'))
df12 = pd.DataFrame(d12)

d14 = json.load(open('data/ohlcv_2m_14oct_1400_1450.json'))
df14 = pd.DataFrame(d14)

def get_stats(df, name, c_target):
    n = len(df)
    dt = 120
    t_inc = n * dt
    t_elap = (n - 1) * dt
    
    gh = df['high'].max()
    gl = df['low'].min()
    rng = gh - gl
    
    idx_h = df['high'].idxmax()
    idx_l = df['low'].idxmin()
    
    first_ext = min(idx_h, idx_l)
    last_ext = max(idx_h, idx_l)
    
    span_ext = last_ext - first_ext
    bars_from_first_ext_to_end = n - 1 - first_ext
    bars_from_last_ext_to_end = n - 1 - last_ext
    
    first_bar = df.iloc[0]
    last_bar = df.iloc[-1]
    
    net_move = last_bar['close'] - first_bar['open']
    path = np.abs(df['close'].diff()).sum()
    
    tot_vol = df['volume'].sum()
    mean_vol = df['volume'].mean()
    end_vol = last_bar['volume']
    
    c_base = round(t_inc * 10 / 183)
    delta_c = c_target - c_base
    
    close_pos = (last_bar['close'] - gl) / rng
    end_body = abs(last_bar['close'] - last_bar['open'])
    end_rng = last_bar['high'] - last_bar['low']
    
    print(f'=== {name} ===')
    print(f'n = {n}, T_inc = {t_inc}s, T_elap = {t_elap}s')
    print(f'C_target = {c_target}, C_base = {c_base}, Delta_C = {delta_c}')
    print(f'High = {gh:.2f} (idx {idx_h}, bar {idx_h+1})')
    print(f'Low  = {gl:.2f} (idx {idx_l}, bar {idx_l+1})')
    print(f'Range = {rng:.2f} pts ({rng*4:.0f} ticks)')
    print(f'Span between extremes = {span_ext} bars = {span_ext*dt}s')
    print(f'Bars from first extreme to END = {bars_from_first_ext_to_end} bars = {bars_from_first_ext_to_end*dt}s')
    print(f'Bars from last extreme to END  = {bars_from_last_ext_to_end} bars = {bars_from_last_ext_to_end*dt}s')
    print(f'Net move = {net_move:.2f} pts, Path = {path:.2f} pts, ER = {abs(net_move)/path:.3f}')
    print(f'End Close Pos in Range = {close_pos:.3f}')
    print(f'End Body = {end_body:.2f}, End Rng = {end_rng:.2f}')
    print(f'End Vol / Mean Vol = {end_vol / mean_vol:.2f}')
    print()

if __name__ == '__main__':
    get_stats(df12, '12-Oct (14:30 to 15:16)', 190)
    get_stats(df14, '14-Oct (14:00 to 14:50)', 191)
