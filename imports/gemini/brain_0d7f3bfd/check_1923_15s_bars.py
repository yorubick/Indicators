import json
from pathlib import Path

ROOT = Path(r"G:\trading\guias\analisis")
preds = json.loads((ROOT / 'C_transicion1923_predicciones.json').read_text(encoding='utf-8'))['cases']
for c in preds:
    if c['id'] == 'C_transicion1923_15':
        ohlc = c['OHLC']
        print("Total bars in 1903 to 1923:15:", len(ohlc))
        # print the last 6 bars
        for idx in range(len(ohlc)-6, len(ohlc)):
            b = ohlc[idx]
            print(f"Bar {idx}: O={b['open']}, H={b['high']}, L={b['low']}, C={b['close']}")
        break

# Also check 19:23:45 candle from C_recorte1903
preds_recorte = json.loads((ROOT / 'C_recorte1903_predicciones.json').read_text(encoding='utf-8'))['cases']
for c in preds_recorte:
    if c['id'] == 'C_recorte1903_15':
        ohlc = c['OHLC']
        print("\nLast 6 bars of 19:03:15 to 19:23:45:")
        for idx in range(len(ohlc)-6, len(ohlc)):
            b = ohlc[idx]
            print(f"Bar {idx}: O={b['open']}, H={b['high']}, L={b['low']}, C={b['close']}")
        break
