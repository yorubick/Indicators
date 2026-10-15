import csv,json
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).parent
def stamp(s):return int(datetime.fromisoformat('2026-10-12T'+s+':00+00:00').timestamp())
cases=json.loads((ROOT/'familia_character.json').read_text())
for case in cases:
 rows=list(csv.DictReader(Path(case['file']).open()))
 if not any(int(r['time'])==stamp(case['start'])for r in rows):rows=list(csv.DictReader((ROOT/'character_manual_15m_1m.csv').open()))
 seg=[{k:float(r[k])for k in ['open','high','low','close']}for r in rows if stamp(case['start'])<=int(r['time'])<=stamp(case['end'])]
 h=max(r['high']for r in seg);l=min(r['low']for r in seg);target=(h+l)/2
 c=case['possible_integer_C_seconds'][0];dt=case['source_seconds']
 errors=[]
 for base in [72,89,100]:
  for scale in [1/27,1/9,1/3,1,3]:
   n=base*c*scale/dt;a=2/(n+1);q=1-a
   weights=[q**(len(seg)-i-1)for i in range(len(seg))]
   predicted=sum(w*r['close']for w,r in zip(weights,seg))/sum(weights)
   errors.append((abs(predicted-target),base,scale,predicted,target))
 print(case['start'],case['end'],dt,c,sorted(errors)[:3])
