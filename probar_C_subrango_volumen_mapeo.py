"""Segunda etapa explícita: primer cruce volumen selecciona subrango."""
import json,sys,math
from analizar_C_fuente_vs_grafico import ROOT
from probar_C_reinicio_subrango import events
from probar_C_volumen import metrics

SPEC={'selectors':['volume_cross_1','volume_cross_1.5'],
 'selection':'First up-cross as specified in C_reinicio_subrango_preregistro.json; inclusive event..END.',
 'mapping':'C=K*selected_n*dt*10/183*volume_feature. Same22 features as prior volume test; one positiveK shared by nine controls; observedC+/-1second.',
 'scope':'Exploratory second stage selected after descriptor audit; labels known. No training32 or validation, no arbitrary per-case coefficients.'}

def main():
    p=ROOT/'C_subrango_volumen_mapeo_preregistro.json'
    if '--spec' in sys.argv:p.write_text(json.dumps(SPEC,indent=2),encoding='utf-8');print('Etapa2 guardada.');return
    assert json.loads(p.read_text())==SPEC
    cases=json.loads((ROOT/'C_matriz_frontera15s_volumen.json').read_text())['cases'];results=[]
    for selector in SPEC['selectors']:
        selected=[]
        for c in cases:
            i,_=events(c['OHLC'],selector)[0];rows=c['OHLC'][i:]
            assert len(rows)>=20
            selected.append({**c,'bars':len(rows),'OHLC':rows})
        fs=[metrics(c) for c in selected];names=sorted(set.intersection(*(set(f) for f in fs)))
        for name in names:
            raw=[c['bars']*c['dt']*10/183*f[name] for c,f in zip(selected,fs)]
            assert all(math.isfinite(v) and v>0 for v in raw)
            lo=max((round(c['C'])-1)/v for c,v in zip(selected,raw));hi=min((round(c['C'])+1)/v for c,v in zip(selected,raw))
            results.append({'selector':selector,'feature':name,'common_K_interval':[lo,hi],'survives9':lo<=hi})
    out={'spec':SPEC,'models':results,'model_count':len(results),'survivors':sum(r['survives9'] for r in results),'training32_used':False,'reserved_validation_used':False}
    (ROOT/'C_subrango_volumen_mapeo_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ['spec','models']},indent=2))

if __name__=='__main__':main()
