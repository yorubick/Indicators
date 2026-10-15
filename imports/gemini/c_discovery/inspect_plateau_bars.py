import json
import pandas as pd

with open(r'G:\trading\guias\analisis\C_1s_salida_meseta_resultados.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

results = d['results']

rows = []
for r in results:
    n = r['bars']
    c_val = r['C']
    high = r['high']
    low = r['low']
    rng = high - low
    last_bar = r['END_OHLCV']
    rows.append({
        'n': n,
        'C': round(c_val),
        'high': high,
        'low': low,
        'range': rng,
        'open': last_bar['open'],
        'h_bar': last_bar['high'],
        'l_bar': last_bar['low'],
        'c_bar': last_bar['close'],
        'v_bar': last_bar['Volume'],
        'break_dir': r['breakout_direction'],
    })

df = pd.DataFrame(rows)
print(df.to_string(index=False))
