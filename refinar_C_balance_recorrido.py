"""Control de resolución numérica del modelo mejor ordenado previamente."""
import json,math
from pathlib import Path
import numpy as np
from probar_C_balance_recorrido import roots,score
from probar_C_estructura import load
ROOT=Path(__file__).parent

def main():
    result=json.loads((ROOT/'C_balance_recorrido.json').read_text())
    best=result['best_training_models'][0];key=tuple(best['model']);branch=best['root_branch']
    prior=json.loads((ROOT/'C_estructura.json').read_text())
    training=[c for c in prior['training_cases']+prior['reserved_cases'] if c['C']>c['dt']]
    test=result['reserved_cases']
    getter=min if branch=='smallest' else max
    sets={};lengths={}
    for count in (1200,12000):
        grid=np.geomspace(1.00001,10000,count);sets[count]=[];lengths[count]=[]
        for c in training+test:
            v,interval,_=load(c);c['interval']=interval
            r=roots(v,grid,only_model=key)
            assert r[key],c
            sets[count].append(r);lengths[count].append(getter(r[key]))
    fine=sets[12000];active=fine[:len(training)]
    ratios=[getter(r[key])*c['dt']/c['C'] for c,r in zip(training,active)]
    K=math.exp(float(np.mean(np.log(ratios))))
    lower=max(getter(r[key])*c['dt']/c['interval']['upper_exclusive'] for c,r in zip(training,active))
    upper=min(getter(r[key])*c['dt']/c['interval']['lower_inclusive'] for c,r in zip(training,active))
    output={'model':key,'branch':branch,'grid_points':[1200,12000],
        'max_relative_root_change':max(abs(b/a-1) for a,b in zip(lengths[1200],lengths[12000])),
        'K_refined_training_only':K,'K_compatible_lower':lower,'K_compatible_upper':upper,
        'K_intersection_nonempty':lower<upper,'training':score(training,active,key,K,branch),
        'reserved':score(test,fine[len(training):],key,K,branch),
        'scope':'Refines only the previous best training model. Finite sign-changing-root search; not a proof about tangent roots or every candidate.'}
    (ROOT/'C_balance_convergencia.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
