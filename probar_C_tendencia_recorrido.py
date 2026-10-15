"""Familia predeclarada; K común calibrado solo en episodios de entrenamiento."""
import math,json
import numpy as np
from pathlib import Path
ROOT=Path(__file__).parent
SHAPES={'one':lambda r,e:1,'1+r':lambda r,e:1+r,'1-r':lambda r,e:1-r,'1+r2':lambda r,e:1+r*r,'1-r2':lambda r,e:1-r*r,'inverse1+r':lambda r,e:1/(1+r),'inverse1-r':lambda r,e:1/(1-r),'inverse1+r2':lambda r,e:1/(1+r*r),'inverse1-r2':lambda r,e:1/(1-r*r),'sqrt1-r2':lambda r,e:math.sqrt(1-r*r),'inverse_sqrt1-r2':lambda r,e:1/math.sqrt(1-r*r),'1+ER':lambda r,e:1+e,'1-ER':lambda r,e:1-e,'inverse1+ER':lambda r,e:1/(1+e),'inverse1-ER':lambda r,e:1/(1-e),'ER':lambda r,e:e,'r2':lambda r,e:r*r}
def shape(case,price,scope,fn):
    rows=case['OHLC'] if scope=='full' else case['OHLC'][-21:];v=np.array([[r[k]for k in ['open','high','low','close']]for r in rows]);o,h,l,c=v.T
    x={'close':c,'hl2':(h+l)/2,'hlc3':(h+l+c)/3,'ohlc4':(o+h+l+c)/4}[price];r=abs(float(np.corrcoef(x,np.arange(len(x)))[0,1]));path=float(np.abs(np.diff(x)).sum());e=float(abs(x[-1]-x[0])/path)if path else 0
    if not math.isfinite(r):return None
    try:y=fn(r,e)*case['bars']*case['dt']*10/183
    except(ZeroDivisionError,ValueError):return None
    return y if math.isfinite(y)and y>0 else None
def q(x,mode):return math.floor(x+.5)if mode=='nearest'else(math.floor(x)if mode=='floor'else math.ceil(x))
def main():
    d=json.loads((ROOT/'C_dataset_verificado.json').read_text());long=[c for c in d['cases']if c['branch']=='long'];train=[c for c in long if c['split']=='training'];test=[c for c in long if c['split']=='validation'];assert all(abs(c['C']-round(c['C']))<1e-7 for c in long)
    records=[]
    for price in ['close','hl2','hlc3','ohlc4']:
        for scope in ['full','last21']:
            for name,fn in SHAPES.items():
                vals=[shape(c,price,scope,fn)for c in train]
                if any(v is None for v in vals):continue
                for mode in ['nearest','floor','ceil']:
                    bounds=[((round(c['C'])-.5,round(c['C'])+.5)if mode=='nearest'else((round(c['C']),round(c['C'])+1)if mode=='floor'else(round(c['C'])-1,round(c['C']))))for c in train]
                    lows=[lo/v for(lo,hi),v in zip(bounds,vals)];highs=[hi/v for(lo,hi),v in zip(bounds,vals)];lower=max(lows);upper=min(highs)
                    # Ceil interval has lower-open/upper-closed; strict nonempty criterion sufficient here.
                    feasible=lower<upper;K=(lower+upper)/2 if feasible else float(np.median([c['C']/v for c,v in zip(train,vals)]))
                    predictions=[q(K*v,mode)for v in vals];errors=[abs(p-round(c['C']))for p,c in zip(predictions,train)]
                    i=lows.index(lower);j=highs.index(upper)
                    rec={'price':price,'scope':scope,'shape':name,'quantizer':mode,'K_training':K,'K_interval':{'lower':lower,'upper':upper,'nonempty':feasible},'training_matches':sum(e==0 for e in errors),'training_cases':len(train),'training_max_error_seconds':max(errors),'conflict_witness':None if feasible else {'lower_case':train[i]['id'],'lower_C':train[i]['C'],'lower_bound':lower,'upper_case':train[j]['id'],'upper_C':train[j]['C'],'upper_bound':upper}}
                    # Only exact-training candidates qualify for validation.
                    if feasible:
                        tv=[shape(c,price,scope,fn)for c in test];rec['validation']={'cases':len(test),'matches':sum(v is not None and q(K*v,mode)==round(c['C'])for c,v in zip(test,tv)),'predictions':[q(K*v,mode)if v is not None else None for v in tv]}
                    records.append(rec)
    records.sort(key=lambda r:(-r['training_matches'],r['training_max_error_seconds'],r['price'],r['scope'],r['shape'],r['quantizer']))
    short=[c for c in d['cases']if c['branch']=='short'];out={'dataset':'C_dataset_verificado.json','counts':d['counts'],'short_rule':{'cases':len(short),'matches':sum(abs(max(c['dt'],c['bars']*c['dt']*10/183)-c['C'])<1e-7 for c in short)},'formula':'short:max(dt,n*dt*10/183); long:quantize(K*n*dt*10/183*g(abs(Pearson(price,index)),ER))','models_tested':len(records),'exact_training_candidates':sum(r['K_interval']['nonempty']for r in records),'scope':'Finite exploratory family, no global long-branch floor. K calibrated only training. Validation labels previously observed by investigators; not prospective or human-blind. No general formula established by rejecting this family.','records':records}
    (ROOT/'C_tendencia_recorrido.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps({**{k:v for k,v in out.items()if k!='records'},'best_training_only':records[:3]},indent=2))
if __name__=='__main__':main()
