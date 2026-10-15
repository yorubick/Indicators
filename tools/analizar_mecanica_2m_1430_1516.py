import json
import pandas as pd
import numpy as np

def main():
    candles = json.load(open('data/ohlcv_2m_1430_1516.json', 'r', encoding='utf-8'))
    df = pd.DataFrame(candles)
    df['time_str'] = df['time'].apply(lambda x: x[11:16])

    print("=== DATASET 2M: 14:30 a 15:16 (24 VELAS) ===")
    print(df[['time_str', 'open', 'high', 'low', 'close', 'volume']])

    # Conocidos C
    known_c = {
        '14:50': 120.0,
        '15:06': 124.5902,
        '15:08': 131.1475,
        '15:10': 124.0,
        '15:12': 153.0,
        '15:14': 146.0,
        '15:16': 190.0
    }

    print("\n=== ANÁLISIS DE LAS VELAS CON C CONOCIDO ===")
    rows = []
    for k, row in df.iterrows():
        t_str = row['time_str']
        if t_str not in known_c:
            continue
        c_val = known_c[t_str]
        sub = df.iloc[:k+1]
        
        n_inc = k + 1
        t_inc = n_inc * 120
        t_elap = k * 120
        
        gh = sub['high'].max()
        gl = sub['low'].min()
        gh_idx = sub['high'].idxmax()
        gl_idx = sub['low'].idxmin()
        
        bs_gh = k - gh_idx
        bs_gl = k - gl_idx
        
        rng = gh - gl
        pos = (row['close'] - gl) / rng if rng > 0 else 0.5
        dist_ext = min(row['close'] - gl, gh - row['close']) / rng if rng > 0 else 0
        
        c_base = round((t_inc * 10) / 183)
        delta_c = c_val - c_base
        
        rows.append({
            'END': t_str,
            'k': k,
            'n_inc': n_inc,
            'C': c_val,
            'C_base': c_base,
            'Delta_C': delta_c,
            'T_inc/C': round(t_inc / c_val, 2),
            'Range_H': gh,
            'Range_L': gl,
            'Height': rng,
            'idx_GH': gh_idx,
            'time_GH': df.iloc[gh_idx]['time_str'],
            'bs_GH': bs_gh,
            'time_GL': df.iloc[gl_idx]['time_str'],
            'bs_GL': bs_gl,
            'ClosePos': round(pos, 3),
            'DistExt': round(dist_ext, 3),
            'BarVol': row['volume']
        })

    res_df = pd.DataFrame(rows)
    print(res_df.to_string(index=False))

if __name__ == '__main__':
    main()
