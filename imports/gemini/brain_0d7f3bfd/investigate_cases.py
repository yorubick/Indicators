import json
import numpy as np

with open(r'G:\trading\guias\analisis\C_evolucion87_resultados.json') as f:
    data13 = json.load(f)
with open(r'G:\trading\guias\analisis\C_evolucion87_predicciones.json') as f:
    pred13 = json.load(f)

full_ohlc_13 = pred13['OHLC']

print("=== OCT 13 CASES ===")
for c in data13['cases']:
    sub = full_ohlc_13[:c['bars']]
    highs = [x['high'] for x in sub]
    lows = [x['low'] for x in sub]
    opens = [x['open'] for x in sub]
    closes = [x['close'] for x in sub]
    rng = max(highs) - min(lows)
    sp = (opens[0] - min(lows)) / rng
    print(f"{c['END']}: bars={c['bars']}, actual_C={c['C']}, rng={rng:.2f}, start_pos={sp:.2f}")
