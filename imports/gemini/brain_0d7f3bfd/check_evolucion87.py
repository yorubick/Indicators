import json

with open(r'G:\trading\guias\analisis\C_evolucion87_resultados.json') as f:
    res = json.load(f)

print("Cases in C_evolucion87_resultados.json:")
for c in res['cases']:
    bars = c['bars']
    end = c['END'][11:16]
    C = c['C']
    rng_h = c['range_high']
    rng_l = c['range_low']
    rng = rng_h - rng_l
    end_ohlc = c['END_OHLC']
    print(f"END={end} | bars={bars} | C={round(C):2d} | High={rng_h} | Low={rng_l} | Range={rng:5.2f} | End_C={end_ohlc['close']}")
