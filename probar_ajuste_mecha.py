import csv,math
from pathlib import Path
from datetime import datetime
def stamp(s):
    return int(datetime.fromisoformat('2026-10-12T'+s+':00+00:00').timestamp())
ROOT=Path(__file__).parent
datasets=[('character_manual_15m_1m.csv','04:45','05:00','high'),
          ('character_manual_15m_1m.csv','04:45','05:05','high'),
          ('character_manual_15m_1m.csv','04:45','05:15','high'),
          ('character_manual_15m_1m.csv','04:45','05:25','high'),
          ('character_recent_20m.csv','19:00','19:20','low')]
for fn,s,e,target in datasets:
    rows=list(csv.DictReader((ROOT/fn).open()))
    segment=[r for r in rows if stamp(s)<=int(r['time'])<=stamp(e)]
    print(s,e,'target',segment[-1][target])
    for init in ['open','high','low','close']:
        for skip in [0,1]:
            def value(n):
                v=float(segment[0][init]);a=2/(n+1)
                for r in segment[skip:]: v+=a*(float(r['close'])-v)
                return v-float(segment[-1][target])
            grid=[1+i*.01 for i in range(9900)]
            roots=[]
            for a,b in zip(grid,grid[1:]):
                if value(a)*value(b)>0:continue
                for _ in range(40):
                    m=(a+b)/2
                    if value(a)*value(m)<=0:b=m
                    else:a=m
                roots.append((a+b)/2)
            print(init,skip,[(round(n,6),round(n*27,6))for n in roots])
