"""Diagnosticos para contrastar modelos de C; no constituye un predictor."""
import csv,json,statistics
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).parent
cases=json.loads((ROOT/'familia_character.json').read_text(encoding='utf-8'))
def stamp(s):return int(datetime.fromisoformat('2026-10-12T'+s+':00+00:00').timestamp())
out=[]
for case in cases:
    rows=list(csv.DictReader(Path(case['file']).open(encoding='utf-8-sig')))
    if not any(int(r['time'])==stamp(case['start'])for r in rows):
        rows=list(csv.DictReader((ROOT/'character_manual_15m_1m.csv').open()))
    seg=[{k:float(r[k])for k in ['open','high','low','close']}for r in rows
         if stamp(case['start'])<=int(r['time'])<=stamp(case['end'])]
    h=max(r['high']for r in seg);l=min(r['low']for r in seg)
    ranges=[r['high']-r['low']for r in seg]
    bodies=[abs(r['close']-r['open'])for r in seg]
    tr=[max(r['high']-r['low'],abs(r['high']-p['close']),abs(r['low']-p['close']))for p,r in zip(seg,seg[1:])]
    c=case['possible_integer_C_seconds'][0];dt=case['source_seconds']
    record={'start':case['start'],'end':case['end'],'C':c,'dt':dt,'bars':len(seg),
            'height':h-l,'mean_range':statistics.mean(ranges),'mean_body':statistics.mean(bodies),
            'mean_tr':statistics.mean(tr),'start_close':seg[0]['close'],'end_close':seg[-1]['close'],
            'end_high':seg[-1]['high'],'end_low':seg[-1]['low'],
            'mean_close':statistics.mean(r['close']for r in seg),
            'end_position':(seg[-1]['close']-l)/(h-l)}
    out.append(record)
    print(case['start'],case['end'],'dt',dt,'C/dt',round(c/dt,4),
          'height/mean range',round((h-l)/record['mean_range'],4),
          'height/mean tr',round((h-l)/record['mean_tr'],4),
          'height/mean body',round((h-l)/record['mean_body'],4),
          'endpos',round(record['end_position'],3))
(ROOT/'caracteristicas_rangos.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
