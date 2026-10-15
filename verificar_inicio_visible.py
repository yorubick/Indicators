"""Contrasta primera curva visible con primer cierre posterior fuera del rango."""
import csv,json
from datetime import datetime,timezone
from pathlib import Path
from identificar_emas import COLUMNS
ROOT=Path(__file__).parent
def stamp(s):return int(datetime.fromisoformat('2026-10-12T'+(s+':00' if len(s)==5 else s)+'+00:00').timestamp())
def fmt(t):return datetime.fromtimestamp(t,timezone.utc).strftime('%H:%M:%S') if t is not None else None
def main():
    cases=json.loads((ROOT/'C_cruce_doble.json').read_text())['cases'];out=[]
    for case in cases:
        with Path(case['file']).open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        start,end=stamp(case['start']),stamp(case['end']);dt=case['dt']
        by={int(r['time']):r for r in rows}
        expected=list(range(start,end+1,dt))
        if not all(t in by for t in expected):
            out.append({'file':case['file'],'eligible':False,'reason':'OHLC del rango incompleto en este archivo'});continue
        seg=[by[t] for t in expected];high=max(float(r['high']) for r in seg);low=min(float(r['low']) for r in seg)
        visible={k:next((int(r['time']) for r in rows if r.get(k)),None) for k in COLUMNS}
        breakout=next((int(r['time']) for r in rows if int(r['time'])>end and (float(r['close'])>high or float(r['close'])<low)),None)
        first=min((t for t in visible.values() if t is not None),default=None)
        out.append({'file':case['file'],'START':case['start'],'END':case['end'],'source_seconds':dt,
            'eligible':True,'range_high':high,'range_low':low,'first_visible':fmt(first),
            'first_close_outside_range':fmt(breakout),'all_layers_same_first_time':len(set(visible.values()))==1,
            'match':first==breakout,'first_visible_by_layer':{k:fmt(t) for k,t in visible.items()}})
    valid=[c for c in out if c['eligible']]
    result={'scope':'Primera aparicion historica de curvas en rangos Manual. No reglas de señales ni prueba intravela.',
        'eligible_cases':len(valid),'matching_cases':sum(c['match'] for c in valid),'cases':out}
    (ROOT/'C_inicio_visible.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'eligible':len(valid),'matching':result['matching_cases'],
        'mismatches':[c for c in valid if not c['match']]},indent=2))
if __name__=='__main__':main()
