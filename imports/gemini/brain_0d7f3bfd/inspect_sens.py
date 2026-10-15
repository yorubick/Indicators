import json
from pathlib import Path

path = Path('G:/trading/guias/analisis/C_sensibilidad_15s.json')
data = json.load(path.open(encoding='utf-8'))
print('--- 15s START sweep (END = 19:20:00) ---')
for c in data['cases']:
    start = c['START_UTC']
    c_val = c['extraction']['compatible_integer_C_seconds']
    interv = c['extraction']['C_seconds_interval']
    low = interv['lower_inclusive']
    high = interv['upper_exclusive']
    print(f"START {start} | C = {c_val} | [{low:.4f}, {high:.4f})")
