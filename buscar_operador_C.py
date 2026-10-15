"""Contraste de una clase concreta de modelos: ajuste de UNA EMA al rango.
No ajusta un predictor estadistico ni afirma identificar el codigo privado.
"""
import csv,json,math
from pathlib import Path
from datetime import datetime
import numpy as np
ROOT=Path(__file__).parent
def stamp(s):return int(datetime.fromisoformat('2026-10-12T'+s+':00+00:00').timestamp())
cases=json.loads((ROOT/'familia_character.json').read_text())
cases=[c for c in cases if c['possible_integer_C_seconds'][0]>c['source_seconds']]
cases.append({'file':str(ROOT/'C_25m_live_confirmado.csv'),'start':'18:55','end':'19:20',
              'source_seconds':60,'possible_integer_C_seconds':[62]})
data=[]
for c in cases:
    rows=list(csv.DictReader(Path(c['file']).open()))
    if not any(int(r['time'])==stamp(c['start'])for r in rows):rows=list(csv.DictReader((ROOT/'character_manual_15m_1m.csv').open()))
    seg=np.array([[float(r[k])for k in ['open','high','low','close']]for r in rows
                  if stamp(c['start'])<=int(r['time'])<=stamp(c['end'])])
    data.append((c,seg))
grid=np.geomspace(1.000001,10000,4000)
alpha=2/(grid+1);q=1-alpha
all_roots={}
for ci,(case,seg) in enumerate(data):
    columns={'open':seg[:,0],'high':seg[:,1],'low':seg[:,2],'close':seg[:,3],
             'hl2':(seg[:,1]+seg[:,2])/2,'hlc3':(seg[:,1]+seg[:,2]+seg[:,3])/3,
             'ohlc4':seg.mean(axis=1)}
    def endpoints(i):
        out={k:float(v[i])for k,v in columns.items()}
        out.update(range_high=float(seg[:,1].max()),range_low=float(seg[:,2].min()),
                   range_mid=float((seg[:,1].max()+seg[:,2].min())/2))
        out['mid_defended_wick']=out['low'] if out['close']>=out['range_mid'] else out['high']
        out['mid_opposite_wick']=out['high'] if out['close']>=out['range_mid'] else out['low']
        out['body_defended_wick']=out['low'] if out['close']>=out['open'] else out['high']
        out['body_opposite_wick']=out['high'] if out['close']>=out['open'] else out['low']
        return out
    for direction in ['forward','reverse']:
        initial=endpoints(0 if direction=='forward'else -1)
        target=endpoints(-1 if direction=='forward'else 0)
        for source,values in columns.items():
            for inclusion in ['all','skip_start','skip_end','skip_both']:
                samples={'all':values,'skip_start':values[1:],'skip_end':values[:-1],
                         'skip_both':values[1:-1]}[inclusion]
                if direction=='reverse':samples=samples[::-1]
                base=np.zeros(len(grid))
                for v in samples:base=q*base+alpha*v
                decay=q**len(samples)
                for seed_name,seed in initial.items():
                    response=base+decay*seed
                    for target_name,t in target.items():
                        residual=response-t
                        indices=np.flatnonzero(residual[:-1]*residual[1:]<0)
                        roots=[]
                        for i in indices:
                            n=grid[i]+(grid[i+1]-grid[i])*(-residual[i])/(residual[i+1]-residual[i])
                            roots.append(float(n/(case['possible_integer_C_seconds'][0]/case['source_seconds'])))
                        key=(direction,source,inclusion,seed_name,target_name)
                        all_roots.setdefault(key,[None]*len(data))[ci]=roots
    print('Processed',case['start'],case['end'],'source',case['source_seconds'],flush=True)
scores=[]
for model,sets in all_roots.items():
    if any(not roots for roots in sets):continue
    for k in sets[0]:
        best=[min(roots,key=lambda value:abs(math.log(value/k)))for roots in sets]
        logmean=sum(map(math.log,best))/len(best)
        spread=max(abs(math.log(v)-logmean)for v in best)
        scores.append({'max_log_deviation':spread,'model':model,
                       'K_by_case':best,'K_geometric_mean':math.exp(logmean)})
scores.sort(key=lambda r:r['max_log_deviation'])
result={'cases':[{'start':c['start'],'end':c['end'],'C':c['possible_integer_C_seconds'][0],
                  'source':c['source_seconds']}for c,s in data],
        'model_count':len(all_roots),'best_models':scores[:20]}
(ROOT/'busqueda_operador_C.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result['best_models'][:3],indent=2))
