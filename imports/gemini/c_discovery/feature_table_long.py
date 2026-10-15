import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = master['cases']

rows = []
for c in cases:
    if c['bars'] >= 21 and c.get('C_Lite') is not None:
        df = pd.DataFrame(c['OHLCV'])
        n = len(df)
        dt = c['dt']
        total_sec = n * dt
        c_val = c['C_Lite']
        
        r_high = df['high'].max()
        r_low = df['low'].min()
        rng = r_high - r_low
        rng_ticks = rng * 4.0
        
        last = df.iloc[-1]
        first = df.iloc[0]
        
        idx_h = df['high'].idxmax()
        idx_l = df['low'].idxmin()
        
        bars_from_high_to_end = n - 1 - idx_h
        bars_from_low_to_end = n - 1 - idx_l
        sec_from_high_to_end = bars_from_high_to_end * dt
        sec_from_low_to_end = bars_from_low_to_end * dt
        
        # Swings and distances
        dist_h_l_bars = abs(idx_h - idx_l)
        dist_h_l_sec = dist_h_l_bars * dt
        
        # TR and ATR
        tr = np.maximum(df['high'] - df['low'], 
                        np.maximum(abs(df['high'] - df['close'].shift(1).fillna(df['open'])),
                                   abs(df['low'] - df['close'].shift(1).fillna(df['open']))))
        atr14 = tr.rolling(14).mean().iloc[-1]
        atr20 = tr.rolling(20).mean().iloc[-1]
        mean_tr = tr.mean()
        sum_tr = tr.sum()
        
        # Volume
        sum_vol = df['volume'].sum()
        mean_vol = df['volume'].mean()
        last_vol = last['volume']
        
        # Price path
        net_move = abs(last['close'] - first['open'])
        path = abs(df['close'].diff()).sum()
        er = net_move / path if path > 0 else 0
        
        rows.append({
            'id': c['id'],
            'dt': dt,
            'n': n,
            'total_sec': total_sec,
            'C': c_val,
            'C_round': round(c_val),
            'rng': rng,
            'rng_ticks': rng_ticks,
            'bars_h_end': bars_from_high_to_end,
            'bars_l_end': bars_from_low_to_end,
            'sec_h_end': sec_from_high_to_end,
            'sec_l_end': sec_from_low_to_end,
            'dist_hl_sec': dist_h_l_sec,
            'atr20': atr20,
            'mean_tr': mean_tr,
            'sum_tr': sum_tr,
            'er': er,
            'sum_vol': sum_vol,
        })

feat_df = pd.DataFrame(rows)
print(f"Total features rows: {len(feat_df)}")
print(feat_df.head(10).to_string())

# Correlations with C
corrs = feat_df.corr(numeric_only=True)['C'].sort_values(ascending=False)
print("\nCorrelations with C:")
print(corrs)
