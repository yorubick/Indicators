import pandas as pd
import numpy as np

df = pd.read_csv(r'G:\trading\guias\analisis\manual\C_startSweep1920_geometria_historia_larga.csv')
df['datetime'] = pd.to_datetime(df['time'], unit='s', utc=True)

# Let's inspect the candles at START timestamps:
# 18:45, 18:54, 18:55, 18:56 with END at 19:20
starts = ['2026-10-12 18:45:00', '2026-10-12 18:54:00', '2026-10-12 18:55:00', '2026-10-12 18:56:00']
end = '2026-10-12 19:20:00'

for st in starts:
    window = df[(df['datetime'] >= st) & (df['datetime'] <= end)].copy()
    n = len(window)
    h = window['high'].max()
    l = window['low'].min()
    rng = h - l
    start_bar = window.iloc[0]
    end_bar = window.iloc[-1]
    
    # Distance of start candle from window extremes
    st_high_dist = h - start_bar['high']
    st_low_dist = start_bar['low'] - l
    # Position of start open and close
    pos_open = (start_bar['open'] - l) / rng
    pos_close = (start_bar['close'] - l) / rng
    
    print(f"--- START: {st} (n={n}) ---")
    print(f"High: {h}, Low: {l}, Range: {rng}")
    print(f"Start bar: Open={start_bar['open']}, High={start_bar['high']}, Low={start_bar['low']}, Close={start_bar['close']}")
    print(f"Pos Open: {pos_open:.4f}, Pos Close: {pos_close:.4f}")
    print(f"End bar Close: {end_bar['close']}, End Pos: {(end_bar['close'] - l)/rng:.4f}")
