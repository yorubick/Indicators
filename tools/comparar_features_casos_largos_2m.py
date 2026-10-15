import json
import pandas as pd
import numpy as np

def analyze():
    data = json.load(open('data/ohlcv_2m_1430_1516.json'))
    df = pd.DataFrame(data)
    
    # Indices of the 4 long cases
    cases = [
        (20, '15:10', 124),
        (21, '15:12', 153),
        (22, '15:14', 146),
        (23, '15:16', 190)
    ]
    
    print("=== COMPARATIVA DE CARACTERÍSTICAS PARA LOS 4 CASOS LARGOS ===")
    records = []
    for idx, t_str, c_val in cases:
        sub = df.iloc[:idx+1].copy()
        n = len(sub)
        
        # Precios de la vela END
        end_o = sub.iloc[-1]['open']
        end_h = sub.iloc[-1]['high']
        end_l = sub.iloc[-1]['low']
        end_c = sub.iloc[-1]['close']
        end_v = sub.iloc[-1]['volume']
        end_rng = end_h - end_l
        end_body = abs(end_c - end_o)
        
        # Rango global
        gh = sub['high'].max()
        gl = sub['low'].min()
        gh_idx = sub['high'].idxmax()
        gl_idx = sub['low'].idxmin()
        tot_rng = gh - gl
        
        # Distancias
        bs_gh = idx - gh_idx
        bs_gl = idx - gl_idx
        dist_gh = gh - end_c
        dist_gl = end_c - gl
        pos_rng = (end_c - gl) / tot_rng
        dist_ext = min(dist_gh, dist_gl) / tot_rng
        
        # Path length
        diffs = np.abs(np.diff(sub['close']))
        path = np.sum(diffs)
        er = abs(end_c - sub.iloc[0]['open']) / path if path > 0 else 0
        
        # True Range
        tr = [sub.iloc[0]['high'] - sub.iloc[0]['low']]
        for i in range(1, len(sub)):
            tr.append(max(sub.iloc[i]['high'] - sub.iloc[i]['low'],
                          abs(sub.iloc[i]['high'] - sub.iloc[i-1]['close']),
                          abs(sub.iloc[i]['low'] - sub.iloc[i-1]['close'])))
        atr14 = np.mean(tr[-14:]) if len(tr) >= 14 else np.mean(tr)
        
        # Volume
        cum_vol = sub['volume'].sum()
        vol_mean = sub['volume'].mean()
        vol_ratio = end_v / vol_mean
        
        # VWAP
        tp = (sub['high'] + sub['low'] + sub['close']) / 3.0
        vwap = np.sum(tp * sub['volume']) / cum_vol
        dist_vwap = end_c - vwap
        
        records.append({
            'END': t_str,
            'C': c_val,
            'T_inc': n * 120,
            'Ratio_T/C': round((n * 120) / c_val, 2),
            'bs_GH': bs_gh,
            'dist_GH': dist_gh,
            'dist_GL': dist_gl,
            'pos_rng': round(pos_rng, 3),
            'dist_ext': round(dist_ext, 3),
            'end_rng': end_rng,
            'end_body': end_body,
            'end_vol': end_v,
            'vol_ratio': round(vol_ratio, 2),
            'dist_vwap': round(dist_vwap, 2),
            'path': round(path, 1),
            'er': round(er, 3),
            'atr14': round(atr14, 2)
        })
        
    res_df = pd.DataFrame(records)
    print(res_df.to_string(index=False))

if __name__ == '__main__':
    analyze()
