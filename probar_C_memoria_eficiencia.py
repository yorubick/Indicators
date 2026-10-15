"""Familia exploratoria acotada de memoria de coeficientes de eficiencia.

No es una afirmación sobre el algoritmo original. Reglas congeladas antes
de calcular; etiquetas locales conocidas, no validación prospectiva.
"""
import itertools,json,sys
from analizar_C_fuente_vs_grafico import ROOT

SPEC={
 'source':['close','hl2'], 'lookback':[3,9,20,27,'growing'],
 'target':'ER=abs(x_t-x_start)/sum(abs(diff(x))) over last L changes or all available changes; ER=0 when path=0. target=(2/31+(2/3-2/31)*ER)**power.',
 'powers':[1,2], 'seeds':['slow','fast','first_target'],
 'initialization':'At first change t=1 seed alpha with (2/31)**power, (2/3)**power or target_1. Process t=2..END; no preSTART history.',
 'memory_lengths':[1,3,9,20,27,81],
 'recurrence':'alpha_t=alpha_previous+2/(M+1)*(target_t-alpha_previous)',
 'mapping':'C=K*dt*(2/alpha_END-1), same K>0 for all nine cases.',
 'gate':'Intersect intervals K implied by observed C +/-1 second. Also count matches after nearest-integer rounding for fixed K=1/scale, scale24,8,72/27,72,216. No per-case parameters.',
 'scope':'360 fixed recurrences. Exploratory known nine overlapping controls; not all recursive models. No training32 or reserved validation unless one common K interval survives all9.'}

def trace(case,source,L,power,seed,M):
    x=[r['close'] if source=='close' else (r['high']+r['low'])/2 for r in case['OHLC']]
    targets=[]
    for t in range(1,len(x)):
        start=0 if L=='growing' else max(0,t-L)
        path=sum(abs(x[i]-x[i-1]) for i in range(start+1,t+1))
        er=abs(x[t]-x[start])/path if path else 0.
        assert -1e-12<=er<=1+1e-12
        targets.append((2/31+(2/3-2/31)*er)**power)
    a={'slow':(2/31)**power,'fast':(2/3)**power,'first_target':targets[0]}[seed]
    history=[a]
    for target in targets[1:]:
        a+=2/(M+1)*(target-a);history.append(a)
    assert all((2/31)**power-1e-12<=v<=(2/3)**power+1e-12 for v in history)
    if M==1:assert abs(a-targets[-1])<1e-12
    return a,history

def main():
    specpath=ROOT/'C_memoria_eficiencia_preregistro.json'
    if '--spec' in sys.argv:
        specpath.write_text(json.dumps(SPEC,indent=2),encoding='utf-8')
        print('Reglas congeladas:360 recurrencias, sin parámetros por caso.');return
    assert json.loads(specpath.read_text())==SPEC
    cases=json.loads((ROOT/'C_matriz_frontera15s.json').read_text())['cases']
    models=[]
    for source,L,power,seed,M in itertools.product(SPEC['source'],SPEC['lookback'],SPEC['powers'],SPEC['seeds'],SPEC['memory_lengths']):
        rows=[];lower=0.;upper=float('inf')
        for c in cases:
            a,history=trace(c,source,L,power,seed,M)
            raw=c['dt']*(2/a-1)
            assert raw>0
            lo=(round(c['C'])-1)/raw;hi=(round(c['C'])+1)/raw
            lower=max(lower,lo);upper=min(upper,hi)
            rows.append({'START':c['START'],'END':c['END'],'C':c['C'],
                         'alpha_END':a,'raw_period_seconds':raw,'K_interval':[lo,hi]})
        fixed=[]
        for scale in [24.,8.,72/27,72.,216.]:
            pred=[int(r['raw_period_seconds']/scale+.5) for r in rows]
            fixed.append({'scale':scale,'predictions':pred,
                          'exact_matches':sum(abs(v-r['C'])<1e-7 for v,r in zip(pred,rows))})
        models.append({'source':source,'lookback':L,'power':power,'seed':seed,'M':M,
                       'common_K_interval':[lower,upper],'survives_all9':lower<=upper,
                       'fixed_scales':fixed,'cases':rows})
    pair_ratios=[]
    for m in models:
        a=next(r for r in m['cases'] if r['START'].endswith('19:03:15+00:00') and r['END'].endswith('19:23:45+00:00'))
        b=next(r for r in m['cases'] if r['START'].endswith('19:03:30+00:00') and r['END'].endswith('19:23:45+00:00'))
        pair_ratios.append(a['raw_period_seconds']/b['raw_period_seconds'])
    out={'spec':SPEC,'models':models,'model_count':len(models),
         'surviving_common_K':sum(m['survives_all9'] for m in models),
         'best_fixed_matches':max(f['exact_matches'] for m in models for f in m['fixed_scales']),
         'pair88_vs61':{'predicted_ratio_min':min(pair_ratios),'predicted_ratio_max':max(pair_ratios),
                         'required_ratio_interval_with_tolerance':[87/62,89/60],
                         'compatible_models':sum(87/62<=v<=89/60 for v in pair_ratios)},
         'training32_used':False,'reserved_validation_used':False}
    (ROOT/'C_memoria_eficiencia_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    best=min(models,key=lambda m:m['common_K_interval'][0]/m['common_K_interval'][1])
    print(json.dumps({k:v for k,v in out.items() if k not in ['spec','models']},indent=2))
    print(json.dumps({'least_incompatible_model':{k:v for k,v in best.items() if k not in ['cases','fixed_scales']},
                      'best_fixed_models':[{'source':m['source'],'L':m['lookback'],'power':m['power'],'seed':m['seed'],'M':m['M'],'fixed':f} for m in models for f in m['fixed_scales'] if f['exact_matches']==out['best_fixed_matches']][:6]},indent=2))

if __name__=='__main__':main()
