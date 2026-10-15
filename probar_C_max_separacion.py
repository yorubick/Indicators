"""Familia acotada: C entero maximiza separación final de EMAs72/89.

No ajusta coeficientes ni selecciona semillas por caso. Si falla la matriz,
no utiliza los32largos de entrenamiento ni la validación para rescatarla.
"""
import json,math,sys
import numpy as np
from analizar_C_fuente_vs_grafico import ROOT

SEEDS=['START_open','START_high','START_low','START_close','bootstrap20_low','bootstrap20_high']
DIVISORS=[3.,9.,27.,1.,1/3]
SPEC={'hypothesis':'Integer C maximizes abs(EMAfast_END-EMAslow_END). Both filters use close; Nfast=72*C/(divisor*dt),Nslow=89*C/(divisor*dt).',
      'candidate_integer_C':[1,600], 'admissibility':'Nfast>=1,Nslow>=1. No global source_seconds floor in long branch.',
      'seed_policies':{'START_OHLC':'Both EMA states initialized at bar0 OHLC seed; process close bars1..END.',
                       'bootstrap20_extrema':'At bar19 initialize both states with minlow/maxhigh of first20bars; process closes20..END. Motivated by empirical short/long boundary, not verified original initialization.'},
      'seeds':SEEDS,'divisors':DIVISORS,'tie_policy':'Smallest C whose score is within1e-12 of maximum in normalized price units.',
      'selection':'No fitted coefficients, no per-case seed choice, no clock/absoluteprice conditions. Thirty fixed candidates, must fit all9 local matrix before any training32 scoring.',
      'scope':'Different from prior endpoint-contact/cross roots: objective is maximum final separation, not a zero-crossing. Tests this finite family only; no general EMA optimization rejection.'}

def scores(case,seed_name,divisor,price_source='close',signed=False):
    assert price_source in ['close','hl2']
    rows=case['OHLC'];dt=case['dt'];Cs=np.arange(1,601,dtype=float)
    nf=72*Cs/(divisor*dt);ns=89*Cs/(divisor*dt);ok=(nf>=1)&(ns>=1)
    Cs=Cs[ok];nf=nf[ok];ns=ns[ok];af=2/(nf+1);ass=2/(ns+1)
    lo=min(r['low'] for r in rows);hi=max(r['high'] for r in rows);R=hi-lo
    assert R>0
    if seed_name.startswith('START_'):
        seed=rows[0][seed_name[6:]];start=1
    else:
        assert len(rows)>=21
        seed=min(r['low'] for r in rows[:20]) if seed_name.endswith('low') else max(r['high'] for r in rows[:20]);start=20
    f=np.full(len(Cs),(seed-lo)/R);s=f.copy()
    for r in rows[start:]:
        price=r['close'] if price_source=='close' else (r['high']+r['low'])/2
        x=(price-lo)/R;f+=af*(x-f);s+=ass*(x-s)
    return Cs,(f-s if signed else np.abs(f-s))

def main(price_source='close',prefix='C_max_separacion'):
    spec=json.loads(json.dumps(SPEC))
    if price_source=='hl2':
        spec['hypothesis']=spec['hypothesis'].replace('Both filters use close','Both filters use HL2=(high+low)/2')
        spec['seed_policies']['START_OHLC']=spec['seed_policies']['START_OHLC'].replace('process close bars','process HL2 bars')
        spec['seed_policies']['bootstrap20_extrema']=spec['seed_policies']['bootstrap20_extrema'].replace('process closes','process HL2 values')
        spec['scope']='Controlled source substitution: HL2 instead of close; all seeds, period factors, objective and tie rules unchanged. Known labels, exploratory test; not prospective validation.'
    if '--spec' in sys.argv:
        (ROOT/f'{prefix}_preregistro.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
        print(json.dumps(spec,indent=2));return
    assert json.loads((ROOT/f'{prefix}_preregistro.json').read_text())==spec,'spec changed'
    cases=json.loads((ROOT/'C_matriz_frontera15s.json').read_text())['cases'];models=[]
    for seed in SEEDS:
        for divisor in DIVISORS:
            records=[]
            for c in cases:
                Cs,obj=scores(c,seed,divisor,price_source);best=float(Cs[np.flatnonzero(obj>=obj.max()-1e-12)[0]])
                original=round(c['C']);obs_idx=np.flatnonzero(Cs==original)
                obs=float(obj[obs_idx[0]]) if len(obs_idx) else None
                records.append({'START':c['START'],'END':c['END'],'C':c['C'],'prediction_C':best,
                                'match':abs(best-c['C'])<1e-7,'objective_at_predicted':float(obj[Cs==best][0]),
                                'objective_at_observed':obs,'strict_improvement_over_observed':obs is not None and float(obj.max())>obs+1e-12,
                                'at_upper_bound':best==600})
            models.append({'seed':seed,'divisor':divisor,'exact_matches':sum(r['match'] for r in records),
                           'MAE':sum(abs(r['prediction_C']-r['C']) for r in records)/len(records),'cases':records})
    survivors=[m for m in models if m['exact_matches']==len(cases)]
    out={'spec':spec,'local_cases':len(cases),'model_count':len(models),'models_exact_all9':len(survivors),
         'training32_scored':False,'reserved_validation_used':False,'models':models}
    if survivors:
        train=[c for c in json.loads((ROOT/'C_dataset_verificado.json').read_text())['cases'] if c['split']=='training' and c['branch']=='long']
        for m in survivors:
            m['training32_results']=[]
            for c in train:
                Cs,obj=scores(c,m['seed'],m['divisor'],price_source);prediction=float(Cs[np.flatnonzero(obj>=obj.max()-1e-12)[0]])
                m['training32_results'].append({'id':c['id'],'C':c['C'],'prediction_C':prediction,'match':abs(prediction-c['C'])<1e-7})
        out['training32_scored']=True
    (ROOT/f'{prefix}_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    best=max(m['exact_matches'] for m in models)
    print(json.dumps({'model_count':len(models),'models_exact_all9':len(survivors),'highest_match_count':best,
                      'models_with_highest_count_count':sum(m['exact_matches']==best for m in models),
                      'models_with_highest_count_first3':[{k:v for k,v in m.items() if k!='cases'} for m in models if m['exact_matches']==best][:3],
                      'training32_scored':out['training32_scored'],'reserved_validation_used':False},indent=2))

if __name__=='__main__':main()
