"""Escalas temporales de pivotes internos; selección solo con datos anteriores.

Predicciones reservadas: cuatro rangos del último barrido. Familia finita;
no inspecciona código protegido ni demuestra independencia entre jornadas.
"""
import csv,json,math
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from probar_C_estructura import load
ROOT=Path(__file__).parent

def largest_close_swing(case):
    """Exact descriptor, not just a duration, for a direct collision test."""
    v,_,_=load(case);x=v[:,3];n=len(x)
    highs=[i for i in range(1,n-1) if x[i]>x[i-1] and x[i]>=x[i+1]]
    lows=[i for i in range(1,n-1) if x[i]<x[i-1] and x[i]<=x[i+1]]
    ordered=sorted([(i,'H',float(x[i])) for i in highs]+[(i,'L',float(x[i])) for i in lows])
    pairs=[(a,b) for a,b in zip(ordered,ordered[1:]) if a[1]!=b[1] and b[0]>a[0]]
    if not pairs:return None
    a,b=max(pairs,key=lambda p:abs(p[1][2]-p[0][2]))
    time=case['start'] if len(case['start'])==8 else case['start']+':00'
    start=int(datetime.fromisoformat('2026-10-12T'+time+'+00:00').timestamp())
    return {'first_UTC':datetime.fromtimestamp(start+a[0]*case['dt'],timezone.utc).isoformat(),
            'first_close':a[2],'first_type':a[1],
            'second_UTC':datetime.fromtimestamp(start+b[0]*case['dt'],timezone.utc).isoformat(),
            'second_close':b[2],'second_type':b[1],'duration_seconds':(b[0]-a[0])*case['dt']}

def metrics(v,dt):
    o,h,l,c=v.T;n=len(c);f={}
    for source,hi,lo in [('wick',h,l),('close',c,c),('hl2',(h+l)/2,(h+l)/2)]:
        for radius in (1,2,3,5,8,13):
            highs=[i for i in range(radius,n-radius) if hi[i]>max(hi[i-radius:i]) and hi[i]>=max(hi[i+1:i+radius+1])]
            lows=[i for i in range(radius,n-radius) if lo[i]<min(lo[i-radius:i]) and lo[i]<=min(lo[i+1:i+radius+1])]
            prefix=f'{source}_r{radius}'
            for side,indices in [('high',highs),('low',lows),('either',sorted(set(highs+lows)))]:
                if not indices:continue
                for offset in (0,1):
                    f[f'{prefix}_{side}_age_first_plus{offset}']=(n-1-indices[0]+offset)*dt
                    f[f'{prefix}_{side}_age_last_plus{offset}']=(n-1-indices[-1]+offset)*dt
                    f[f'{prefix}_{side}_start_first_plus{offset}']=(indices[0]+offset)*dt
                    f[f'{prefix}_{side}_start_last_plus{offset}']=(indices[-1]+offset)*dt
                if len(indices)>1:
                    gaps=np.diff(indices)*dt
                    for label,value in [('min',min(gaps)),('max',max(gaps)),('mean',np.mean(gaps)),('median',np.median(gaps)),('first',gaps[0]),('last',gaps[-1])]:
                        f[f'{prefix}_{side}_gap_{label}']=float(value)
            pairs=[]
            # Adjacent opposite-side pivots; simultaneous wick extrema excluded.
            ordered=sorted([(i,'H',hi[i]) for i in highs]+[(i,'L',lo[i]) for i in lows])
            for a,b in zip(ordered,ordered[1:]):
                if a[1]!=b[1] and b[0]>a[0]:pairs.append((abs(b[2]-a[2]),(b[0]-a[0])*dt,a[0],b[0]))
            if pairs:
                for label,pair in [('largest_move',max(pairs,key=lambda p:p[0])),('smallest_move',min(pairs,key=lambda p:p[0])),('first',pairs[0]),('last',pairs[-1])]:
                    f[f'{prefix}_opposite_{label}_duration']=float(pair[1])
                    f[f'{prefix}_opposite_{label}_end_age']=float((n-1-pair[3]+1)*dt)
    # Price-reversal threshold anchored to the selected range height. This is
    # a specified zigzag variant, not an assertion about TradingView's zigzag.
    for source,x in [('close',c),('hl2',(h+l)/2)]:
        for fraction in (.025,.05,.10,.15,.20,.25,.333333333333,.5):
            threshold=(h.max()-l.min())*fraction
            points=[0];extreme=0;direction=0
            for i in range(1,n):
                if direction==0:
                    if abs(x[i]-x[0])>=threshold:direction=1 if x[i]>x[0] else -1;extreme=i
                elif direction>0:
                    if x[i]>=x[extreme]:extreme=i
                    elif x[extreme]-x[i]>=threshold:points.append(extreme);direction=-1;extreme=i
                else:
                    if x[i]<=x[extreme]:extreme=i
                    elif x[i]-x[extreme]>=threshold:points.append(extreme);direction=1;extreme=i
            if len(points)>1:
                gaps=np.diff(points)*dt;prefix=f'{source}_zigzag_{fraction:.4f}'
                for label,value in [('min',min(gaps)),('max',max(gaps)),('mean',np.mean(gaps)),('median',np.median(gaps)),('first',gaps[0]),('last',gaps[-1])]:
                    f[f'{prefix}_gap_{label}']=float(value)
                f[f'{prefix}_last_age']=float((n-points[-1])*dt)
    return {k:float(x) for k,x in f.items() if x>0}

def evaluate(cases,name,K,rounded):
    predictions=[];matches=[]
    for c in cases:
        raw=K*c['metrics'][name]
        p=max(c['dt'],math.floor(raw+.5) if rounded else raw)
        predictions.append(p)
        matches.append(c['interval']['lower_inclusive']<=p<c['interval']['upper_exclusive'])
    return {'predictions':predictions,'interval_matches':sum(matches),
            'median_relative_error':float(np.median([abs(p/c['C']-1) for p,c in zip(predictions,cases)])),
            'max_relative_error':max(abs(p/c['C']-1) for p,c in zip(predictions,cases))}

def main():
    prior=json.loads((ROOT/'C_estructura.json').read_text())
    training=prior['training_cases']+prior['reserved_cases']
    new=json.loads((ROOT/'C_barrido_ampliado.json').read_text())['new_controls']
    reserved=[{'file':c['extraction']['file'],'start':c['START_UTC'],'end':c['END_UTC'],'dt':15,
               'C':c['extraction']['compatible_integer_C_seconds'][0]} for c in new]
    for case in training+reserved:
        v,interval,fallback=load(case)
        case['interval']=interval;case['metrics']=metrics(v,case['dt'])
    # Feature availability alone is checked in the reserved windows; C is not
    # used to choose K or rank models. Every candidate uses one common K.
    shared=set.intersection(*(set(c['metrics']) for c in training+reserved))
    scores=[]
    for name in sorted(shared):
        for rounded in (False,True):
            active=[c for c in training if c['C']>c['dt']]
            lower=max((c['C']-.5 if rounded else c['interval']['lower_inclusive'])/c['metrics'][name] for c in active)
            upper=min((c['C']+.5 if rounded else c['interval']['upper_exclusive'])/c['metrics'][name] for c in active)
            # Flooring further constrains the upper bound, but cannot restore
            # an already empty non-floor intersection.
            for c in training:
                if c['C']==c['dt']:
                    bound=(c['C']+.5 if rounded else c['interval']['upper_exclusive'])/c['metrics'][name]
                    upper=min(upper,bound)
            K=math.exp(float(np.mean([math.log(c['C']/c['metrics'][name]) for c in active])))
            scores.append({'metric':name,'round_seconds':rounded,'K_training_only':K,
                'K_lower':lower,'K_upper':upper,'exact_feasible_training':lower<upper,
                'training':evaluate(training,name,K,rounded),'reserved':evaluate(reserved,name,K,rounded)})
    scores.sort(key=lambda q:(q['training']['max_relative_error'],q['training']['median_relative_error']))
    sweep=json.loads((ROOT/'C_barrido_ampliado.json').read_text())['cases']
    groups={}
    for c in sweep:
        case={'file':c['file'],'start':c['START_UTC'],'end':'19:20:00','dt':15,'C':c['C']}
        descriptor=largest_close_swing(case)
        key=json.dumps(descriptor,sort_keys=True)
        group=groups.setdefault(key,{'swing':descriptor,'cases':[]})
        group['cases'].append({'START_UTC':case['start'],'C':case['C']})
    collisions=[g for g in groups.values() if len({c['C'] for c in g['cases']})>1]
    out={'formula':'C=max(source_seconds, K*duration_metric); optional nearest integer second',
         'training_count':len(training),'reserved_count':len(reserved),'metrics_available_all_cases':len(shared),
         'tested_models':len(scores),'exact_feasible_training':sum(s['exact_feasible_training'] for s in scores),
         'best_training_models':scores[:10],'reserved_cases':reserved,'identical_largest_swing_different_C':collisions,
         'selection':'K and ranking use only earlier 34 cases; four latest cases are contrasted afterwards. Same-date overlapping windows; not independent market validation.',
         'scope':'Specified local pivot and reversal-threshold rules, selections and common linear scale only. Empty feasibility interval rejects exact common-K fit, not all pivot algorithms.'}
    (ROOT/'C_giros_internos.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ('reserved_cases','best_training_models')},indent=2))
    print(json.dumps(scores[0],indent=2))

if __name__=='__main__':main()
