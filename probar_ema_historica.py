import csv
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).parent
def stamp(s):return int(datetime.fromisoformat('2026-10-12T'+s+':00+00:00').timestamp())
for fn,end,side in [('character_manual_15m_1m.csv','05:00','high'),('character_manual_15m_1m.csv','05:05','high'),('character_manual_15m_1m.csv','05:15','high'),('character_manual_15m_1m.csv','05:25','high'),('character_recent_20m.csv','19:20','low')]:
    rows=[r for r in csv.DictReader((ROOT/fn).open())if int(r['time'])<=stamp(end)]
    closes=[float(r['close'])for r in rows];target=float(rows[-1][side])
    def f(n):
        v=closes[0];a=2/(n+1)
        for c in closes[1:]:v+=a*(c-v)
        return v-target
    roots=[]
    grid=[1+i*.1 for i in range(15000)]
    for a,b in zip(grid,grid[1:]):
        if f(a)*f(b)>0:continue
        for _ in range(35):
            m=(a+b)/2
            if f(a)*f(m)<=0:b=m
            else:a=m
        roots.append((a+b)/2)
    print(end,side,target,'roots',roots)
