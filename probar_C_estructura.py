"""Busqueda acotada de escalas de trayectoria, con rangos reservados.

No extrae codigo privado ni afirma un generador de C. Los intervalos de C
proceden de los diez plots originales; OHLC debe cubrir todo el rango.
"""
import csv,json,math
from itertools import combinations
from pathlib import Path
from datetime import datetime
import numpy as np
from obtener_C import recover
ROOT=Path(__file__).parent

def stamp(s):
    if len(s)==5:s+=':00'
    return int(datetime.fromisoformat('2026-10-12T'+s+'+00:00').timestamp())

def load(case):
    start,end=stamp(case['start']),stamp(case['end']);dt=case['dt']
    rows=list(csv.DictReader(Path(case['file']).open(encoding='utf-8-sig')))
    required=list(range(start,end+1,dt))
    available={int(r['time']):r for r in rows}
    fallback=None
    if not all(t in available for t in required):
        assert dt==60 and case['start'].startswith('04:45'),case
        fallback=ROOT/'character_manual_15m_1m.csv'
        available={int(r['time']):r for r in csv.DictReader(fallback.open(encoding='utf-8-sig'))}
    assert all(t in available for t in required),case
    values=np.array([[float(available[t][k]) for k in ('open','high','low','close')] for t in required])
    extraction=recover(Path(case['file']))
    assert extraction['compatible_integer_C_seconds']==[case['C']],case
    return values,extraction['C_seconds_interval'],str(fallback) if fallback else None

def features(v):
    o,h,l,c=v.T;n=len(c);height=h.max()-l.min();diff=np.diff(c)
    ranges=h-l;bodies=abs(c-o)
    tr=np.maximum.reduce([ranges[1:],abs(h[1:]-c[:-1]),abs(l[1:]-c[:-1])])
    f={'bars':float(n),'steps':float(n-1),'sqrt_steps':math.sqrt(n-1)}
    for name,a in [('range',ranges),('body',bodies),('TR',tr),('change',abs(diff))]:
        for stat,x in [('mean',np.mean(a)),('rms',np.sqrt(np.mean(a*a))),('median',np.median(a))]:
            if x>0:f['height_over_'+name+'_'+stat]=height/x
    if np.std(c)>0:f['height_over_close_std']=height/np.std(c)
    if np.std(diff)>0:f['height_over_change_std']=height/np.std(diff)
    path=abs(diff).sum();net=abs(c[-1]-c[0])
    if path>0:
        f['path_over_height']=path/height
        f['efficiency']=max(net/path,1e-6)
        f['steps_efficiency']=(n-1)*max(net/path,1e-6)
    f['extrema_gap']=float(max(abs(int(np.argmax(h))-int(np.argmin(l))),1))
    f['age_high']=float(n-int(np.argmax(h)))
    f['age_low']=float(n-int(np.argmin(l)))
    for name,x in [('close',c),('hl2',(h+l)/2),('hlc3',(h+l+c)/3)]:
        changes=np.diff(x);nonzero=changes[changes!=0]
        reversals=np.count_nonzero(nonzero[1:]*nonzero[:-1]<0)
        f[name+'_mean_sign_run']=(n-1)/(reversals+1)
        for radius in (1,2,3,5):
            pivots=[i for i in range(radius,n-radius) if
                    x[i]>max(x[i-radius:i]) and x[i]>=max(x[i+1:i+radius+1]) or
                    x[i]<min(x[i-radius:i]) and x[i]<=min(x[i+1:i+radius+1])]
            if len(pivots)>1:
                gaps=np.diff(pivots)
                f[f'{name}_pivot{radius}_mean_gap']=float(np.mean(gaps))
                f[f'{name}_pivot{radius}_median_gap']=float(np.median(gaps))
        detrended=x-np.polyval(np.polyfit(np.arange(n),x,1),np.arange(n))
        if np.std(detrended)>0:
            f[name+'_height_over_residual_std']=height/np.std(detrended)
            ac=np.correlate(detrended,detrended,mode='full')[n-1:]/np.dot(detrended,detrended)
            for threshold in (0,0.5,math.exp(-1)):
                below=np.flatnonzero(ac[1:]<threshold)
                f[f'{name}_acf_{threshold:.3f}']=float(below[0]+1 if len(below) else n)
    return f

def evaluate(cases,shape,K):
    predictions=[max(c['dt'],K*c['dt']*shape(c)) for c in cases]
    return {'median_relative_error':float(np.median([abs(p/c['C']-1) for p,c in zip(predictions,cases)])),
            'max_relative_error':float(max(abs(p/c['C']-1) for p,c in zip(predictions,cases))),
            'interval_matches':int(sum(c['interval']['lower_inclusive']<=p<c['interval']['upper_exclusive'] for p,c in zip(predictions,cases))),
            'predictions_seconds':predictions}

def main():
    training=json.loads((ROOT/'C_cruce_doble.json').read_text())['cases']
    # Add floor cases without admitting holdout measurements to training.
    old=json.loads((ROOT/'familia_character.json').read_text())
    training += [{'file':c['file'],'start':c['start'],'end':c['end'],'dt':c['source_seconds'],
                  'C':c['possible_integer_C_seconds'][0]} for c in old if c['possible_integer_C_seconds'][0]==c['source_seconds']]
    reserved=[]
    for r in json.loads((ROOT/'C_agregacion.json').read_text())['ranges']:
        for c in r['cases']:
            reserved.append({'file':c['extraction']['file'],'start':c['first_source_open'][11:19],
                'end':c['last_source_open'][11:19],'dt':c['source_seconds'],
                'C':c['extraction']['compatible_integer_C_seconds'][0]})
    for case in training+reserved:
        v,interval,fallback=load(case)
        case.update(features=features(v),interval=interval,bars=len(v),OHLC_fallback=fallback)
    shared=set.intersection(*(set(c['features']) for c in training+reserved))
    scores=[]
    definitions=[(name,None,exponent,0) for name in sorted(shared) for exponent in (-2,-1,-0.5,0.5,1,2)]
    definitions += [(a,b,p,q) for a,b in combinations(sorted(shared),2) for p,q in ((1,1),(1,-1),(-1,1),(-1,-1))]
    for name,second,exponent,second_exponent in definitions:
            shape=lambda c: c['features'][name]**exponent * (c['features'][second]**second_exponent if second else 1)
            # Fit only non-floor training observations; floor is an empirical option.
            ratios=[c['C']/(c['dt']*shape(c)) for c in training if c['C']>c['dt']]
            K=math.exp(float(np.mean(np.log(ratios))))
            train=evaluate(training,shape,K)
            # Necessary exact feasibility: all non-floor K intervals must intersect.
            lower=max(c['interval']['lower_inclusive']/(c['dt']*shape(c)) for c in training if c['C']>c['dt'])
            upper=min(c['interval']['upper_exclusive']/(c['dt']*shape(c)) for c in training if c['C']>c['dt'])
            scores.append({'feature':name,'power':exponent,'second_feature':second,'second_power':second_exponent,'K_training_only':K,
                'nonfloor_K_interval_intersection':{'lower':float(lower),'upper':float(upper),'exists':bool(lower<upper)},
                'training':train,'reserved':evaluate(reserved,shape,K)})
    scores.sort(key=lambda x:x['training']['max_relative_error'])
    out={'formula':'C_prediction=max(source_seconds,K*source_seconds*feature**power*second_feature**second_power)',
         'training_cases':training,'reserved_cases':reserved,'tested_models':len(scores),
         'exact_training_candidates':sum(x['nonfloor_K_interval_intersection']['exists'] for x in scores),
         'selection':'Rank only by worst training relative error; reserved results never used to fit K or select model.',
         'scope':'Finite feature family. Reserved cases overlap training in market date; three 18:00 cases extend the window and two-minute resolution was absent from training. Not independent market validation. Floor is empirical, not established internal rule.',
         'best_training_models':scores[:10]}
    (ROOT/'C_estructura.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ('training_cases','reserved_cases','best_training_models')},indent=2))
    print(json.dumps(scores[0],indent=2))

if __name__=='__main__':main()
