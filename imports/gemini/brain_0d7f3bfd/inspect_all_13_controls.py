import json
from pathlib import Path

ROOT = Path(r"G:\trading\guias\analisis")

all_new = []
for tag in ['replica24','rama24_resolucion','transicion1923','prefijo192345','recorte1903']:
    p_pred = ROOT / f'C_{tag}_predicciones.json'
    p_res = ROOT / f'C_{tag}_resultados.json'
    if p_pred.exists() and p_res.exists():
        preds = json.loads(p_pred.read_text(encoding='utf-8'))['cases']
        results = json.loads(p_res.read_text(encoding='utf-8'))['cases']
        by_id = {c['id']: c for c in preds}
        for r in results:
            c = by_id[r['id']]
            ohlc = c['OHLC']
            highs = [x['high'] for x in ohlc]
            lows = [x['low'] for x in ohlc]
            opens = [x['open'] for x in ohlc]
            closes = [x['close'] for x in ohlc]
            rng = max(highs) - min(lows)
            dt = c.get('dt', 60)
            bars = c.get('bars', len(ohlc))
            act_c = r['C']
            t_span = (bars - 1) * dt
            
            all_new.append({
                'id': c['id'],
                'tag': tag,
                'dt': dt,
                'bars': bars,
                't_span_s': t_span,
                'act_C': act_c,
                'rng': rng,
                'start_pos': (opens[0] - min(lows)) / rng if rng > 0 else 0.5,
                'end_pos': (closes[-1] - min(lows)) / rng if rng > 0 else 0.5,
                'START': c['START'],
                'END': c['END']
            })

import pandas as pd
df = pd.DataFrame(all_new)
print("=== ALL 13 ADDITIONAL CONTROLS ===")
print(df[['id', 'tag', 'dt', 'bars', 't_span_s', 'act_C', 'rng', 'start_pos', 'START', 'END']].to_string())
