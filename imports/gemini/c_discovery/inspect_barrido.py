import json

with open(r"G:\trading\guias\analisis\C_barrido_END_1855_1920_1924_15s.json", "r", encoding="utf-8") as f:
    barrido = json.load(f)

cases = barrido["cases"]
print(f"Number of cases in barrido: {len(cases)}")

for i, c in enumerate(cases):
    end = c["END"]
    c_val = c["C_Lite"]
    ohlcv = c["OHLCV"]
    # Last candle in ohlcv is the END candle
    last_bar = ohlcv[-1]
    n_bars = len(ohlcv)
    print(f"[{i:2d}] END: {end} | n: {n_bars:3d} | C: {c_val:6.2f} | Last bar: O={last_bar['open']}, H={last_bar['high']}, L={last_bar['low']}, C={last_bar['close']}, V={last_bar['volume']}")
