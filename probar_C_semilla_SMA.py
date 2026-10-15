"""EMA inicializada con media de un bloque, ajustada al precio de END."""
import json,math
from pathlib import Path
import numpy as np
from probar_C_estructura import load
ROOT=Path(__file__).parent
def roots(v,grid):
    o,h,l,c=v.T
    cols={'open':o,'high':h,'low':l,'close':c,'hl2':(h+l)/2,'hlc3':(h+l+c)/3,'ohlc4':v.mean(axis=1)}
    targets={k:float(x[-1]) for k,x in cols.items()};result={};a=2/(grid+1)
    for source,x in cols.items():
        for count in (2,3,5,8,13,21):
            if len(x)<=count:
                for target in targets:result[(source,count,target)]=[]
                continue
            ema=np.full(len(grid),float(np.mean(x[:count])))
            for price in x[count:]:ema+=a*(price-ema)
            for target,t in targets.items():
                f=ema-t;idx=np.flatnonzero(f[:-1]*f[1:]<0)
                result[(source,count,target)]=[float(grid[i]+(grid[i+1]-grid[i])*(-f[i])/(f[i+1]-f[i])) for i in idx]
    return result
def convex_obstruction(v,key):
    source,count,target=key;o,h,l,c=v.T
    cols={'open':o,'high':h,'low':l,'close':c,'hl2':(h+l)/2,'hlc3':(h+l+c)/3,'ohlc4':v.mean(axis=1)}
    x=cols[source]
    if len(x)<=count:return None
    values=[float(np.mean(x[:count]))]+[float(p) for p in x[count:]]
    t=float(cols[target][-1]);low=min(values);high=max(values)
    impossible=t<low or t>high or (low<high and (t==low or t==high))
    return {'target':t,'response_convex_min':low,'response_convex_max':high} if impossible else None
def main():
    prior=json.loads((ROOT/'C_estructura.json').read_text());train=prior['training_cases']+prior['reserved_cases']
    train=[c for c in train if c['C']>c['dt']]
    test=[{'file':c['extraction']['file'],'start':'18:55:00','end':c['END_UTC'],'dt':15,'C':c['C']} for c in json.loads((ROOT/'C_END_barrido.json').read_text())['cases']]
    grid=np.geomspace(1.00001,10000,3000);sets=[];arrays=[]
    for case in train+test:
        v,interval,_=load(case);case['interval']=interval;case['bars']=len(v);arrays.append(v);sets.append(roots(v,grid))
    models=[];coverage=[]
    for key in sets[0]:
        missing=[i for i,r in enumerate(sets[:len(train)]) if not r[key]]
        witnesses=[]
        for i,v in enumerate(arrays[:len(train)]):
            obstruction=convex_obstruction(v,key)
            if obstruction:witnesses.append({'case_index':i,**obstruction})
        coverage.append({'model':key,'missing_training_cases':missing,'convex_obstructions':witnesses})
        if missing:continue
        for branch,choose in [('smallest',min),('largest',max)]:
            ratios=[choose(r[key])*c['dt']/c['C'] for c,r in zip(train,sets)]
            K=math.exp(float(np.mean(np.log(ratios))))
            lo=max(choose(r[key])*c['dt']/c['interval']['upper_exclusive'] for c,r in zip(train,sets))
            hi=min(choose(r[key])*c['dt']/c['interval']['lower_inclusive'] for c,r in zip(train,sets))
            held=[]
            for c,r in zip(test,sets[len(train):]):
                pred=choose(r[key])*c['dt']/K if r[key] else None
                held.append({'END':c['end'],'actual_C':c['C'],'prediction':pred,
                    'compatible':pred is not None and c['interval']['lower_inclusive']<=pred<c['interval']['upper_exclusive']})
            models.append({'model':key,'branch':branch,'K':K,'K_lower':lo,'K_upper':hi,'exact_common_K':lo<hi,
                'max_relative_training_error':max(abs(K/r-1) for r in ratios),'latest_END_results':held})
    models.sort(key=lambda m:m['max_relative_training_error'])
    out={'training_count':len(train),'latest_END_count':len(test),'endpoint_models':len(sets[0]),
        'endpoint_models_with_roots_all_latest_END':sum(all(r[k] for r in sets[len(train):]) for k in sets[0]),
        'root_branch_models':len(sets[0])*2,'models_with_roots_all_training':len(models),
        'exact_common_K_count':sum(m['exact_common_K'] for m in models),'best_training_models':models[:10],
        'endpoint_models_with_convex_obstruction':sum(bool(c['convex_obstructions']) for c in coverage),
        'coverage':coverage,'training_cases':train,'latest_END_cases':test,
        'scope':'Finite SMA seed windows 2,3,5,8,13,21; forward EMA processes only bars after seed window; 7 price sources and 7 END targets; N=K*C/dt. K/branch selected from earlier cases, latest END windows are overlapping diagnostic checks, not independent validation. Only sign-changing roots N in (1,10000).'}
    (ROOT/'C_semilla_SMA.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ('coverage','training_cases','latest_END_cases','best_training_models')},indent=2))
    print(json.dumps(models[0] if models else min(coverage,key=lambda c:len(c['missing_training_cases'])),indent=2))
if __name__=='__main__':main()
