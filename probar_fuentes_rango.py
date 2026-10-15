import csv
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).parent
def stamp(s):return int(datetime.fromisoformat('2026-10-12T'+s+':00+00:00').timestamp())
sources={'close':lambda r:float(r['close']), 'open':lambda r:float(r['open']),
         'high':lambda r:float(r['high']),'low':lambda r:float(r['low']),
         'hl2':lambda r:(float(r['high'])+float(r['low']))/2,
         'ohlc4':lambda r:sum(float(r[k])for k in ['open','high','low','close'])/4}
rows=list(csv.DictReader((ROOT/'character_recent_20m.csv').open()))
seg=[r for r in rows if stamp('19:00')<=int(r['time'])<=stamp('19:20')]
target=float(seg[-1]['low'])
for source,fn in sources.items():
 for seed in [float(seg[0]['close']),min(float(r['low'])for r in seg),max(float(r['high'])for r in seg)]:
    def f(n):
        v=seed;a=2/(n+1)
        for r in seg:v+=a*(fn(r)-v)
        return v-target
    roots=[]
    grid=[1+i*.02 for i in range(5000)]
    for a,b in zip(grid,grid[1:]):
        if f(a)*f(b)>0:continue
        for _ in range(30):
            m=(a+b)/2
            if f(a)*f(m)<=0:b=m
            else:a=m
        roots.append((a+b)/2)
    print(source,seed,roots)
