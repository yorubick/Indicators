import csv,json
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).parent
def stamp(s):return int(datetime.fromisoformat('2026-10-12T'+s+':00+00:00').timestamp())
cases=json.loads((ROOT/'familia_character.json').read_text(encoding='utf-8'))
sources={'close':lambda r:r['close'],'open':lambda r:r['open'],
         'hl2':lambda r:(r['high']+r['low'])/2,
         'hlc3':lambda r:(r['high']+r['low']+r['close'])/3,
         'ohlc4':lambda r:sum(r.values())/4}
for case in cases:
 rows=list(csv.DictReader(Path(case['file']).open()))
 if not any(int(r['time'])==stamp(case['start'])for r in rows):rows=list(csv.DictReader((ROOT/'character_manual_15m_1m.csv').open()))
 seg=[{k:float(r[k])for k in ['open','high','low','close']}for r in rows if stamp(case['start'])<=int(r['time'])<=stamp(case['end'])]
 c=case['possible_integer_C_seconds'][0];dt=case['source_seconds']
 print(case['start'],case['end'],'dt',dt,'C',c)
 candidates=[]
 for reference in [72,89,100]:
  for family in [3,9,27]:
   n=reference*c/(family*dt)
   if n<1:continue
   for source,fn in sources.items():
    for include in [True,False]:
     v=seg[0]['close'];alpha=2/(n+1)
     for r in seg[1:] if include else seg[1:-1]:v+=alpha*(fn(r)-v)
     for side in ['high','low']:
      candidates.append((abs(v-seg[-1][side]),reference,family,source,include,side,v))
 print(sorted(candidates)[:5])
