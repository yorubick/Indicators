"""Busqueda finita: escala EMA definida por contacto con velas interiores.

No descubre codigo privado. N=K*C/dt, semillas explicitas, primer/ultimo
contacto en orden de procesamiento y minimo/maximo N de todos los contactos.
Raices por cambios de signo en una malla logaritmica; no prueba imposibilidad.
"""
import csv,json,math
from pathlib import Path
from datetime import datetime
import numpy as np
ROOT=Path(__file__).parent
def stamp(s):
    return int(datetime.fromisoformat('2026-10-12T'+(s+':00' if len(s)==5 else s)+'+00:00').timestamp())
def load(case):
    rows=list(csv.DictReader(Path(case['file']).open(encoding='utf-8-sig')))
    if not any(int(r['time'])==stamp(case['start']) for r in rows):
        rows=list(csv.DictReader((ROOT/'character_manual_15m_1m.csv').open()))
    return np.array([[float(r[k]) for k in ('open','high','low','close')] for r in rows
        if stamp(case['start'])<=int(r['time'])<=stamp(case['end'])])
def search(points=1200):
    cases=json.loads((ROOT/'C_cruce_doble.json').read_text())['cases']
    grid=np.geomspace(1.00001,10000,points);alpha=2/(grid+1)
    fitted={}
    for case in cases:
        seg=load(case)
        sources={'close':seg[:,3],'hl2':seg[:,1:3].mean(axis=1),
                 'hlc3':seg[:,1:].mean(axis=1),'ohlc4':seg.mean(axis=1)}
        for direction in ('forward','reverse'):
            point=seg[0 if direction=='forward' else -1]
            seeds=dict(zip(('open','high','low','close'),point))
            seeds.update(range_high=seg[:,1].max(),range_low=seg[:,2].min(),range_mid=(seg[:,1].max()+seg[:,2].min())/2)
            for source,values in sources.items():
                for inclusion,sl in (('all',slice(None)),('skip_start',slice(1,None)),
                                     ('skip_end',slice(None,-1)),('skip_both',slice(1,-1))):
                    samples=values[sl];targets=seg[sl]
                    if direction=='reverse':samples=samples[::-1];targets=targets[::-1]
                    for seed_name,seed in seeds.items():
                        for timing in ('before','after'):
                            v=np.full(len(grid),seed);roots={key:[] for key in ('open','high','low','close')}
                            for index,(price,target_row) in enumerate(zip(samples,targets)):
                                if timing=='after':v+=alpha*(price-v)
                                # First and last source candles are excluded as targets.
                                # Interior contact is the newly tested hypothesis.
                                if 0<index<len(samples)-1:
                                    for key,target in zip(('open','high','low','close'),target_row):
                                        residual=v-target
                                        cross=np.flatnonzero(residual[:-1]*residual[1:]<0)
                                        found=[]
                                        for j in cross:
                                            n=grid[j]+(grid[j+1]-grid[j])*(-residual[j])/(residual[j+1]-residual[j])
                                            found.append(float(n*case['dt']/case['C']))
                                        if found:roots[key].append((index,found))
                                if timing=='before':v+=alpha*(price-v)
                            for target,groups in roots.items():
                                selections={}
                                if groups:
                                    all_roots=[r for _,rs in groups for r in rs]
                                    selections={'min_N':min(all_roots),'max_N':max(all_roots),
                                        'first_contact_min_N':min(groups[0][1]),'first_contact_max_N':max(groups[0][1]),
                                        'last_contact_min_N':min(groups[-1][1]),'last_contact_max_N':max(groups[-1][1])}
                                for selection in ('min_N','max_N','first_contact_min_N','first_contact_max_N','last_contact_min_N','last_contact_max_N'):
                                    key=(direction,source,inclusion,seed_name,timing,target,selection)
                                    fitted.setdefault(key,[]).append(selections.get(selection))
        print('Processed',case['start'],case['end'],case['dt'],flush=True)
    scores=[]
    for model,ks in fitted.items():
        if any(x is None for x in ks):continue
        center=sum(math.log(x) for x in ks)/len(ks)
        scores.append({'model':model,'K_geometric_mean':math.exp(center),'K_by_case':ks,
            'max_log_deviation':max(abs(math.log(x)-center) for x in ks)})
    scores.sort(key=lambda x:x['max_log_deviation'])
    output={'cases':cases,'model_count':len(fitted),'models_with_contacts_in_all_cases':len(scores),
        'length_grid':[float(grid[0]),float(grid[-1]),points],'best_models':scores[:5],
        'scope':'Contactos EMA interiores con semillas y selecciones enumeradas. Malla finita, no prueba general.'}
    (ROOT/'C_contacto_interior.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    print(json.dumps({'model_count':len(fitted),'models_with_contacts_in_all_cases':len(scores),'best':scores[:1]},indent=2))
if __name__=='__main__':search()
