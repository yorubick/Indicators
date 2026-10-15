"""Intervalos de pesos compatibles con máxima separación final.

EMA lineal con semillas fijas: D(lambda)=lambda*Dclose+(1-lambda)*Dhl2.
Exige un lambda común; no ajusta pesos individuales a cada selección.
"""
import json,sys
import numpy as np
from probar_C_max_separacion import ROOT,SEEDS,DIVISORS,scores

SPEC={'source':'lambda*close+(1-lambda)*HL2, lambda in[0,1], fixed across all9cases',
      'objective':'C integer1..600 must maximize absolute ENDgap of same72/89EMAfamily',
      'seeds':SEEDS,'divisors':DIVISORS,'tolerance_normalized':1e-10,
      'constraint':'For every competitorj: abs(Dobserved(lambda)) >= abs(Dj(lambda))-tolerance. Necessary condition; allows all maximizing ties, weaker than smallestCtie policy.',
      'method':'Exact affine dependence of signed gap onlambda; split at sign zeros, solve linear inequalities, intersect closed intervals across competitors and cases. Float arithmetic, no sampling of lambda.',
      'scope':'Fixed generator family only; includes HL2(lambda0),close(lambda1),HLC3(lambda1/3). Labels known, exploratory feasibility test, not prospective. No validation data scored.'}

def merge(xs):
    out=[]
    for a,b in sorted(xs):
        if a>b:continue
        if out and a<=out[-1][1]:out[-1]=(out[-1][0],max(b,out[-1][1]))
        else:out.append((a,b))
    return out

def intersect(xs,ys):
    return merge([(max(a,c),min(b,d)) for a,b in xs for c,d in ys if max(a,c)<=min(b,d)])

def permitted(bo,ao,bj,aj):
    # D=b+a*lambda, signed state difference in normalized prices.
    cuts=[0.,1.]
    for b,a in [(bo,ao),(bj,aj)]:
        if a!=0 and 0<(-b/a)<1:cuts.append(-b/a)
    cuts=sorted(set(cuts));out=[];tol=SPEC['tolerance_normalized']
    for l,h in zip(cuts,cuts[1:]):
        mid=(l+h)/2;so=1 if bo+ao*mid>=0 else -1;sj=1 if bj+aj*mid>=0 else -1
        q0=so*bo-sj*bj+tol;q1=so*ao-sj*aj
        if q1==0:
            if q0>=0:out.append((l,h))
        elif q1>0:
            lower=max(l,-q0/q1)
            if lower<=h:out.append((lower,h))
        else:
            upper=min(h,-q0/q1)
            if l<=upper:out.append((l,upper))
    return merge(out)

def main():
    if '--spec' in sys.argv:
        (ROOT/'C_mezcla_separacion_preregistro.json').write_text(json.dumps(SPEC,indent=2),encoding='utf-8')
        print(json.dumps(SPEC,indent=2));return
    assert json.loads((ROOT/'C_mezcla_separacion_preregistro.json').read_text())==SPEC
    cases=json.loads((ROOT/'C_matriz_frontera15s.json').read_text())['cases'];models=[]
    for seed in SEEDS:
        for divisor in DIVISORS:
            region=[(0.,1.)];audit=[]
            for c in cases:
                Cs,dc=scores(c,seed,divisor,'close',signed=True);Ch,dh=scores(c,seed,divisor,'hl2',signed=True)
                assert np.array_equal(Cs,Ch)
                obs=np.flatnonzero(Cs==round(c['C']))
                assert len(obs)==1
                i=int(obs[0]);slope=dc-dh;local=[(0.,1.)];last_constraint=None
                for j in range(len(Cs)):
                    if i==j:continue
                    local=intersect(local,permitted(float(dh[i]),float(slope[i]),float(dh[j]),float(slope[j])))
                    last_constraint={'competitor_C':float(Cs[j]),'Dobserved_affine':[float(dh[i]),float(slope[i])],
                                     'Dcompetitor_affine':[float(dh[j]),float(slope[j])]}
                    if not local:break
                region=intersect(region,local)
                audit.append({'START':c['START'],'END':c['END'],'C':c['C'],
                              'case_lambda_intervals':local,'joint_lambda_intervals_after_case':region,
                              'last_constraint_processed':last_constraint})
                if not region:break
            models.append({'seed':seed,'divisor':divisor,'feasible_lambda_intervals':region,'cases_processed':len(audit),'audit':audit})
    out={'spec':SPEC,'models':models,'feasible_models':sum(bool(m['feasible_lambda_intervals']) for m in models),
         'training32_scored':False,'reserved_validation_used':False}
    (ROOT/'C_mezcla_separacion_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'models':len(models),'feasible_models':out['feasible_models'],
                      'cases_until_rejection':[m['cases_processed'] for m in models],
                      'training32_scored':False,'reserved_validation_used':False},indent=2))

if __name__=='__main__':main()
