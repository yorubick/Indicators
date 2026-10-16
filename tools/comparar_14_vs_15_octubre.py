import json
import pandas as pd
import numpy as np

d14 = json.load(open('data/ohlcv_2m_14oct_1400_1454.json'))
# Add 14:56 candle for 14-Oct from user telemetry context if available, or analyze up to 14:54
# Wait, user tested 14:00 to 14:56 on 14-Oct (29 bars) and 15-Oct (29 bars)
df14 = pd.DataFrame(d14)

d15 = json.load(open('data/ohlcv_2m_15oct_1400_1456.json'))
df15 = pd.DataFrame(d15)

print(f"14-Oct bars: {len(df14)}, 15-Oct bars: {len(df15)}")

def analyze_box(df, name, C_official):
    n = len(df)
    dt = 120
    T_elap = (n - 1) * dt
    T_inc = n * dt
    
    gh = df['high'].max()
    gl = df['low'].min()
    rng = gh - gl
    
    first = df.iloc[0]
    last = df.iloc[-1]
    
    net_move = last['close'] - first['open']
    abs_net_move = abs(net_move)
    path = np.abs(df['close'].diff()).sum()
    er = abs_net_move / path if path > 0 else 0
    
    # ATR 2m
    tr = np.maximum(df['high'] - df['low'], 
                    np.maximum(abs(df['high'] - df['close'].shift(1)), 
                               abs(df['low'] - df['close'].shift(1))))
    atr = tr.mean()
    
    # Volume
    tot_vol = df['volume'].sum()
    mean_vol = df['volume'].mean()
    
    # Extremes timing
    idx_h = df['high'].idxmax()
    idx_l = df['low'].idxmin()
    time_h = df.iloc[idx_h]['time'][11:16]
    time_l = df.iloc[idx_l]['time'][11:16]
    
    bs_h = n - 1 - idx_h
    bs_l = n - 1 - idx_l
    
    # Position of close in range
    pos = (last['close'] - gl) / rng if rng > 0 else 0.5
    
    # Last bar metrics
    last_rng = last['high'] - last['low']
    last_body = last['close'] - last['open']
    
    print(f"\n==========================================")
    print(f"ANÁLISIS: {name} (C Oficial = {C_official} s)")
    print(f"==========================================")
    print(f"n={n} velas, T_elap={T_elap}s, T_inc={T_inc}s")
    print(f"High: {gh:.2f} (a las {time_h}, hace {bs_h} velas)")
    print(f"Low:  {gl:.2f} (a las {time_l}, hace {bs_l} velas)")
    print(f"Rango de Caja: {rng:.2f} pts ({rng*4:.0f} ticks)")
    print(f"Start Open: {first['open']:.2f}, End Close: {last['close']:.2f}")
    print(f"Net Move: {net_move:+.2f} pts, Path: {path:.2f} pts, ER: {er:.4f}")
    print(f"ATR(2m): {atr:.2f} pts")
    print(f"Volumen Total: {tot_vol}, Volumen Medio: {mean_vol:.1f}")
    print(f"Posición Cierre en Caja: {pos:.4f}")
    print(f"Última Vela: O={last['open']}, H={last['high']}, L={last['low']}, C={last['close']}")
    print(f"Última Vela: Rango={last_rng:.2f}, Body={last_body:+.2f}")
    print(f"Relación T/C: {T_elap / C_official:.4f} (elap), {T_inc / C_official:.4f} (inc)")
    print(f"C_base = round(T/18.3) = {round(T_elap/18.3)} s (elap), {round(T_inc/18.3)} s (inc)")
    print(f"Delta C = {C_official - round(T_elap/18.3)} s (elap), {C_official - round(T_inc/18.3)} s (inc)")

analyze_box(df14, "14 de Octubre", 195)
analyze_box(df15, "15 de Octubre", 227)
