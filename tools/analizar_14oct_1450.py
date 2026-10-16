import json
import pandas as pd
import numpy as np

def main():
    d14 = json.load(open('data/ohlcv_2m_14oct_1400_1450.json'))
    df14 = pd.DataFrame(d14)
    df14['time_str'] = df14['time'].apply(lambda x: x[11:16])
    
    d12 = json.load(open('data/ohlcv_2m_1430_1516.json'))
    df12 = pd.DataFrame(d12)
    df12['time_str'] = df12['time'].apply(lambda x: x[11:16])
    
    print("=== ANÁLISIS DE LA VELA END DEL 14 DE OCTUBRE (14:50) ===")
    gh14 = df14['high'].max()
    gl14 = df14['low'].min()
    rng14 = gh14 - gl14
    
    end14 = df14.iloc[-1]
    pos14 = (end14['close'] - gl14) / rng14
    dist_ext14 = min(end14['close'] - gl14, gh14 - end14['close']) / rng14
    
    end_rng14 = end14['high'] - end14['low']
    end_body14 = abs(end14['close'] - end14['open'])
    lower_wick14 = min(end14['open'], end14['close']) - end14['low']
    upper_wick14 = end14['high'] - max(end14['open'], end14['close'])
    
    mean_vol14 = df14['volume'].mean()
    vol_ratio14 = end14['volume'] / mean_vol14
    
    print(f"Global High: {gh14:.2f} at {df14.iloc[df14['high'].idxmax()]['time_str']}")
    print(f"Global Low:  {gl14:.2f} at {df14.iloc[df14['low'].idxmin()]['time_str']}")
    print(f"Total Range: {rng14:.2f} pts")
    print(f"Close Pos:   {pos14:.4f} (dist_ext = {dist_ext14:.4f})")
    print(f"End Candle:  Open={end14['open']}, High={end14['high']}, Low={end14['low']}, Close={end14['close']}")
    print(f"End Rng:     {end_rng14:.2f}, Body={end_body14:.2f}, LowerWick={lower_wick14:.2f}, UpperWick={upper_wick14:.2f}")
    print(f"LowerWick%:  {lower_wick14 / end_rng14:.3f}, UpperWick%: {upper_wick14 / end_rng14:.3f}")
    print(f"End Volume:  {end14['volume']} (Mean: {mean_vol14:.1f}, Ratio: {vol_ratio14:.2f})")
    print(f"C Oficial:   191 s (Base = {round(26 * 120 * 10 / 183)} s, Delta = {191 - round(26 * 120 * 10 / 183)} s)")

if __name__ == '__main__':
    main()
