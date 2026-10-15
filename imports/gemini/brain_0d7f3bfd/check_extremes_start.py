import json

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

for st in ['19:00', '19:01', '19:02', '19:03', '19:04']:
    c = next(x for x in data['cases'] if x['START'].startswith(f'2026-10-12T{st}') and x['bars'] == 21)
    ohlc = c['OHLC']
    highs = [x['high'] for x in ohlc]
    lows = [x['low'] for x in ohlc]
    h_val = max(highs)
    l_val = min(lows)
    imax = highs.index(h_val)
    imin = lows.index(l_val)
    time_h = ohlc[imax]['time']
    time_l = ohlc[imin]['time']
    print(f"START {st}: C={round(c['C']):2d} | High={h_val:.2f} at bar {imax} (t={time_h}) | Low={l_val:.2f} at bar {imin} (t={time_l}) | Range={h_val - l_val:.2f}")
