import json

with open(r'G:\trading\guias\analisis\C_evolucion87_predicciones.json') as f:
    data = json.load(f)

bars = data['OHLC']
print(f"Total OHLC bars: {len(bars)}")
print("First bar (06:25):", bars[0])
start_open = bars[0]['open']
low = 30644.5
high = 30675.25
rng = high - low
start_pos = (start_open - low) / rng
print(f"Start open: {start_open}, Range: {rng}, Start pos: {start_pos:.3f}")
