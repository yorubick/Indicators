import json, csv, datetime
from pathlib import Path
import numpy as np

# Load all 34 training cases from C_cruce_doble.json or probar_C_estructura.py
root = Path('G:/trading/guias/analisis')
sens_15s = json.load(open(root / 'C_sensibilidad_15s.json', encoding='utf-8'))
barrido = json.load(open(root / 'C_barrido_ampliado.json', encoding='utf-8'))

# Let's inspect all cases from barrido
ref_path = root / 'C_barrido_15s_start1854_estabilizado.csv'
rows = list(csv.DictReader(ref_path.open(encoding='utf-8-sig')))
candle_map = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows}

def to_ts(time_str):
    return int(datetime.datetime.fromisoformat('2026-10-12T' + time_str + '+00:00').timestamp())

cases_data = []
for c in barrido['cases']:
    s_ts = to_ts(c['START_UTC'])
    e_ts = to_ts('19:20:00')
    sub = [candle_map[t] for t in range(s_ts, e_ts + 1, 15) if t in candle_map]
    highs = [x['high'] for x in sub]
    lows = [x['low'] for x in sub]
    closes = [x['close'] for x in sub]
    opens = [x['open'] for x in sub]
    
    cases_data.append({
        'START': c['START_UTC'],
        'C': c['C'],
        'bars': len(sub),
        'high': max(highs),
        'low': min(lows),
        'open': opens[0],
        'close': closes[-1],
        'range': max(highs) - min(lows),
        'ticks': (max(highs) - min(lows)) / 0.25,
        'net_change': closes[-1] - opens[0],
        'sub': sub
    })

print(f"{'START':10s} | {'C':4s} | {'High':9s} | {'Low':9s} | {'Range':6s} | {'Ticks':6s} | {'Open':9s} | {'Close':9s} | {'Net':6s}")
for d in cases_data:
    print(f"{d['START']:10s} | {d['C']:4d} | {d['high']:9.2f} | {d['low']:9.2f} | {d['range']:6.2f} | {d['ticks']:6.0f} | {d['open']:9.2f} | {d['close']:9.2f} | {d['net_change']:+6.2f}")
