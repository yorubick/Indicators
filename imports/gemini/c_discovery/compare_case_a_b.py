import json
import pandas as pd

with open(r'G:\trading\guias\analisis\C_1s_salida_meseta_resultados.json', 'r', encoding='utf-8') as f:
    d_salida = json.load(f)

with open(r'G:\trading\guias\analisis\C_1s_cruce_START_resultados.json', 'r', encoding='utf-8') as f:
    d_cruce = json.load(f)

# Case A: START 14:04:00, END 14:04:32 (from salida meseta, bars=33)
case_A = [r for r in d_salida['results'] if r['bars'] == 33][0]

# Case B: START 14:04:01, END 14:04:33 (from cruce START, bars=33)
case_B = d_cruce['results'][1]

print("CASE A:")
print(f"START: {case_A['START_UTC']}, END: {case_A['END_UTC']}, bars: {case_A['bars']}, C: {case_A['C']}")
print(f"high: {case_A['high']}, low: {case_A['low']}")
print("Last bar A:", case_A['END_OHLCV'])

print("\nCASE B:")
print(f"START: {case_B['START_UTC']}, END: {case_B['END_UTC']}, bars: {case_B['bars']}, C: {case_B['C']}")
print(f"high: {case_B['high']}, low: {case_B['low']}")
print("Last bar B:", case_B['OHLC'][-1])

print("\nFirst bar A:", case_A['OHLC'][0])
print("First bar B:", case_B['OHLC'][0])
