"""Ajusta recurrencia de plots 5s procesando precios observados 1s.
No atribuye C hasta verificar fuente, alineacion y familia.
"""
import csv,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).parent
def read(name):
    with (ROOT/name).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def fit():
    fine=read('C_auto_OHLC_1s_END_y_wick.csv');plots=read('C_auto_END1920_wick1930_30871_5s.csv')
    by={int(r['time']):r for r in fine};sources={'close':lambda r:float(r['close']),
        'hl2':lambda r:(float(r['high'])+float(r['low']))/2,
        'ohlc4':lambda r:sum(float(r[k]) for k in ('open','high','low','close'))/4}
    out=[]
    for source,fn in sources.items():
        for offset in (-1,0,4,5):
            for gaps in ('skip','carry_close'):
                pairs=[]
                for p,r in zip(plots,plots[1:]):
                    t=int(r['time']);prev=int(p['time'])
                    if t-prev!=5 or not p['Extra cloud 1'] or not r['Extra cloud 1']:continue
                    if not 1791833100<=t<1791833550:continue # 19:25--19:32:30 UTC
                    values=[];last=by.get(prev+offset)
                    for s in range(prev+offset+1,t+offset+1):
                        row=by.get(s)
                        if row:values.append(fn(row));last=row
                        elif gaps=='carry_close' and last:values.append(float(last['close']))
                    if values:pairs.append((float(p['Extra cloud 1']),float(r['Extra cloud 1']),values))
                def cost(n):
                    a=2/(n+1);errs=[]
                    for y,z,values in pairs:
                        for x in values:y+=a*(x-y)
                        errs.append(y-z)
                    return sum(e*e for e in errs)/len(errs)
                grid=np.geomspace(2,100000,100);idx=min(range(len(grid)),key=lambda i:cost(grid[i]))
                lo=grid[max(0,idx-1)];hi=grid[min(len(grid)-1,idx+1)]
                for _ in range(70):
                    m1=lo+(hi-lo)*.381966;m2=lo+(hi-lo)*.618034
                    if cost(m1)<cost(m2):hi=m2
                    else:lo=m1
                n=(lo+hi)/2
                out.append({'source':source,'offset':offset,'missing_seconds':gaps,'N_1s':n,
                    'pairs':len(pairs),'rmse':math.sqrt(cost(n)),'cost_integer_N':math.sqrt(cost(round(n)))})
    out.sort(key=lambda x:x['rmse'])
    (ROOT/'C_auto_fuente_candidatos.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out[:5],indent=2))
if __name__=='__main__':fit()
