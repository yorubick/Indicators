"""Escala AR(1) en ventanas prefijadas; nunca selecciona ventana por C."""
import json,math
from pathlib import Path
import numpy as np
from probar_C_estructura import load
ROOT=Path(__file__).parent
def metrics(v):
    o,h,l,c=v.T;n=len(v)
    windows={'full':(0,n),'last_half':(n//2,n),'last_quarter':(3*n//4,n),
        'after_last_high':(int(np.flatnonzero(h==h.max())[-1]),n),
        'after_last_low':(int(np.flatnonzero(l==l.min())[-1]),n)}
    for k in (8,13,21,34,55):windows['last_'+str(k)]=(n-k,n) if n>=k else None
    sources={'close':c,'hl2':(h+l)/2,'hlc3':(h+l+c)/3,'ohlc4':v.mean(axis=1)}
    result={}
    for win,bounds in windows.items():
        for source,x in sources.items():
            for transform in ('level','linear_residual','difference'):
                for sign in ('positive','absolute'):
                    for scale in ('EMA_period','e_fold_time'):
                        key=(win,source,transform,sign,scale);result[key]=None
                        if bounds is None:continue
                        a,b=bounds;y=x[a:b].copy()
                        if len(y)<5:continue
                        if transform=='linear_residual':
                            t=np.arange(len(y));y-=np.polyval(np.polyfit(t,y,1),t)
                        elif transform=='difference':y=np.diff(y)
                        lag=y[:-1];next_=y[1:];lag=lag-lag.mean();next_=next_-next_.mean()
                        variance=float(lag@lag)
                        if variance<=1e-20:continue
                        phi=float(lag@next_)/variance
                        if sign=='absolute':phi=abs(phi)
                        if not 0<phi<1:continue
                        result[key]=(1+phi)/(1-phi) if scale=='EMA_period' else -1/math.log(phi)
    return result
def main():
    old=json.loads((ROOT/'C_estructura.json').read_text());train=[c for c in old['training_cases']+old['reserved_cases'] if c['C']>c['dt']]
    test=[{'file':c['extraction']['file'],'start':'18:55:00','end':c['END_UTC'],'dt':15,'C':c['C']} for c in json.loads((ROOT/'C_END_barrido.json').read_text())['cases']]
    sets=[]
    for c in train+test:
        v,interval,_=load(c);c['interval']=interval;sets.append(metrics(v))
    scores=[];coverage=[]
    for key in sets[0]:
        missing=[i for i,m in enumerate(sets[:len(train)]) if m[key] is None]
        coverage.append({'model':key,'valid_training_cases':len(train)-len(missing),'missing_training_indices':missing})
        if missing:continue
        shape=[m[key]*c['dt'] for c,m in zip(train,sets)]
        K=math.exp(float(np.mean(np.log([c['C']/s for c,s in zip(train,shape)]))))
        lo=max(c['interval']['lower_inclusive']/s for c,s in zip(train,shape))
        hi=min(c['interval']['upper_exclusive']/s for c,s in zip(train,shape))
        held=[]
        for c,m in zip(test,sets[len(train):]):
            pred=max(c['dt'],K*c['dt']*m[key]) if m[key] is not None else None
            held.append({'END':c['end'],'C':c['C'],'prediction':pred,
                'interval_match':pred is not None and c['interval']['lower_inclusive']<=pred<c['interval']['upper_exclusive']})
        scores.append({'model':key,'K_training_only':K,'K_lower':lo,'K_upper':hi,'exact_common_K':lo<hi,
            'max_relative_training_error':max(abs(max(c['dt'],K*s)/c['C']-1) for c,s in zip(train,shape)),
            'latest_END_results':held})
    scores.sort(key=lambda s:s['max_relative_training_error']);coverage.sort(key=lambda c:-c['valid_training_cases'])
    out={'training_count':len(train),'latest_END_count':len(test),'tested_models':len(sets[0]),
        'models_defined_all_training':len(scores),'models_exact_common_K':sum(s['exact_common_K'] for s in scores),
        'best_training_models':scores[:10],'best_coverage':coverage[:10],'training_cases':train,'latest_END_cases':test,
        'scope':'AR(1) slope with intercept; fixed windows, sources, transforms; no clipping phi. positive and absolute variants require 0<phi<1. C=max(dt,K*dt*scale), floor empirical. Model and K ranking uses previous ranges only. Latest END windows overlap date and are diagnostic, not independent validation.'}
    (ROOT/'C_memoria_interna.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ('training_cases','latest_END_cases','best_training_models','best_coverage')},indent=2))
    print(json.dumps(scores[0] if scores else coverage[0],indent=2))
if __name__=='__main__':main()
