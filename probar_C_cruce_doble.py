"""Contrasta C como cruce de dos EMAs al final del rango.
Modelo: Nrapida=K*C/dt, Nlenta=r*Nrapida. No afirma identificar C.
"""
import csv,json,math
from pathlib import Path
from datetime import datetime
import numpy as np
ROOT=Path(__file__).parent
def stamp(s):
    if len(s)==5:s+=':00'
    return int(datetime.fromisoformat('2026-10-12T'+s+'+00:00').timestamp())
old=json.loads((ROOT/'familia_character.json').read_text())
cases=[{'file':c['file'],'start':c['start'],'end':c['end'],'dt':c['source_seconds'],
        'C':c['possible_integer_C_seconds'][0]}for c in old
       if c['possible_integer_C_seconds'][0]>c['source_seconds']]
new=json.loads((ROOT/'C_sensibilidad_15s.json').read_text())
for c in new['cases']+new['END_controls']+[new['matched_coverage_control']]:
    cases.append({'file':c['extraction']['file'],'start':c['START_UTC'],'end':c['END_UTC'],
                  'dt':15,'C':c['extraction']['compatible_integer_C_seconds'][0]})
unique={}
for c in cases:unique[(stamp(c['start']),stamp(c['end']),c['dt'])]=c
cases=list(unique.values())
grid=np.geomspace(1.00001,10000,1600)
ratios=[89/72,84/78]
roots_by_model={}
for ci,case in enumerate(cases):
    rows=list(csv.DictReader(Path(case['file']).open(encoding='utf-8-sig')))
    if not any(int(r['time'])==stamp(case['start'])for r in rows):
        rows=list(csv.DictReader((ROOT/'character_manual_15m_1m.csv').open()))
    seg=np.array([[float(r[k])for k in ['open','high','low','close']]for r in rows
                  if stamp(case['start'])<=int(r['time'])<=stamp(case['end'])])
    assert len(seg)>2
    sources={'close':seg[:,3],'hl2':seg[:,1:3].mean(axis=1),
             'hlc3':seg[:,1:].mean(axis=1),'ohlc4':seg.mean(axis=1)}
    for direction in ['forward','reverse']:
        point=seg[0 if direction=='forward'else -1]
        seeds=dict(zip(['open','high','low','close'],point))
        seeds.update(range_high=seg[:,1].max(),range_low=seg[:,2].min(),
                     range_mid=(seg[:,1].max()+seg[:,2].min())/2)
        for inclusion in ['all','skip_start','skip_end','skip_both']:
            for source,values in sources.items():
                samples={'all':values,'skip_start':values[1:],'skip_end':values[:-1],
                         'skip_both':values[1:-1]}[inclusion]
                if direction=='reverse':samples=samples[::-1]
                for ratio in ratios:
                    a=2/(grid+1);b=2/(grid*ratio+1)
                    q=1-a;s=1-b
                    fast=np.zeros(len(grid));slow=np.zeros(len(grid))
                    for value in samples:
                        fast=q*fast+a*value;slow=s*slow+b*value
                    decay_fast=q**len(samples);decay_slow=s**len(samples)
                    for seed_fast_name,seed_fast in seeds.items():
                        for seed_slow_name,seed_slow in seeds.items():
                            residual=fast+decay_fast*seed_fast-slow-decay_slow*seed_slow
                            crossings=np.flatnonzero(residual[:-1]*residual[1:]<0)
                            roots=[]
                            for i in crossings:
                                length=grid[i]+(grid[i+1]-grid[i])*(-residual[i])/(residual[i+1]-residual[i])
                                roots.append(float(length*case['dt']/case['C']))
                            key=(direction,inclusion,source,ratio,seed_fast_name,seed_slow_name)
                            roots_by_model.setdefault(key,[None]*len(cases))[ci]=roots
    print('Processed',case['start'],case['end'],case['dt'],flush=True)
scores=[]
for model,sets in roots_by_model.items():
    if any(not roots for roots in sets):continue
    for initial in sets[0]:
        best=[min(roots,key=lambda x:abs(math.log(x/initial)))for roots in sets]
        center=sum(math.log(x)for x in best)/len(best)
        spread=max(abs(math.log(x)-center)for x in best)
        scores.append({'model':model,'max_log_deviation':spread,
                       'K_geometric_mean':math.exp(center),'K_by_case':best})
scores.sort(key=lambda r:r['max_log_deviation'])
output={'cases':cases,'model_count':len(roots_by_model),
        'models_with_root_in_all_cases':len({tuple(s['model'])for s in scores}),
        'length_grid':[1.00001,10000,1600],'best_models':scores[:5],
        'scope':'Cruce de dos EMAs con semillas indicadas y K comun. No cubre reglas dinamicas ni todos los filtros.'}
(ROOT/'C_cruce_doble.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
print(json.dumps(output['best_models'][:1],indent=2))
