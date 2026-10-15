import csv,json,statistics
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).parent
def stamp(s):return int(datetime.fromisoformat('2026-10-12T'+s+':00+00:00').timestamp())
cases=json.loads((ROOT/'familia_character.json').read_text())
sources={'close':lambda r:r['close'],'open':lambda r:r['open'],
         'high':lambda r:r['high'],'low':lambda r:r['low'],
         'hl2':lambda r:(r['high']+r['low'])/2,
         'hlc3':lambda r:(r['high']+r['low']+r['close'])/3}
results={}
for case in cases:
 c=case['possible_integer_C_seconds'][0];dt=case['source_seconds']
 if c==dt:continue
 rows=list(csv.DictReader(Path(case['file']).open()))
 if not any(int(r['time'])==stamp(case['start'])for r in rows):rows=list(csv.DictReader((ROOT/'character_manual_15m_1m.csv').open()))
 seg=[{k:float(r[k])for k in ['open','high','low','close']}for r in rows if stamp(case['start'])<=int(r['time'])<=stamp(case['end'])]
 for base in [72,89,100]:
  for family in [3,9,27,1]:
   n=base*c/(family*dt);a=2/(n+1)
   if n<1:continue
   for source,fn in sources.items():
    for seed in ['open','high','low','close']:
     for include in ['all','skip_end','skip_start','skip_both']:
      subset={'all':seg,'skip_end':seg[:-1],'skip_start':seg[1:],'skip_both':seg[1:-1]}[include]
      v=seg[-1][seed]
      for r in reversed(subset):v+=a*(fn(r)-v)
      err=min(abs(v-seg[0][s])for s in ['high','low'])
      key=(base,family,source,seed,include)
      results.setdefault(key,[]).append(err)
scores=sorted([(statistics.mean(e),max(e),key,e)for key,e in results.items()])
for score in scores[:15]:print(score)
