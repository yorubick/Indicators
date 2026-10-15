import json
import pandas as pd

with open(r"G:\trading\guias\analisis\C_barrido_END_1855_1920_1924_15s.json", "r", encoding="utf-8") as f:
    barrido = json.load(f)

cases = barrido["cases"]

rows = []
for c in cases:
    ohlcv = c["OHLCV"]
    df = pd.DataFrame(ohlcv)
    last = df.iloc[-1]
    rows.append({
        'END': c['END'].split('T')[1][:8],
        'C': c['C_Lite'],
        'open': last['open'],
        'high': last['high'],
        'low': last['low'],
        'close': last['close'],
        'vol': last['volume'],
    })

res = pd.DataFrame(rows)
print(res.to_string(index=False))
