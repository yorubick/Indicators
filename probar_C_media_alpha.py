"""Límite de mediaalpha para ventanas completas fijas de2..80velas.

No ajusta función de rugosidad. alpha_t>=0 es cualquier función fija
de losOHLC de la ventana, sin estado externo ni dependenciadeSTART.
"""
import json,sys
from analizar_C_fuente_vs_grafico import ROOT

SPEC={'pair':'START19:03:15(C88,n83) vs START19:03:30(C61,n82), same END19:23:45,dt15',
      'model':'alpha_t=f(complete rolling window of L OHLC candles), nonnegative, same function for both cases; arithmetic mean across all complete windows fromSTART toEND.',
      'period_mapping':'N_eff=2/mean(alpha)-1; C=N_eff*dt/scale; scale in[24,8,72/27,72,216].',
      'lookbacks':list(range(2,81)),
      'generous_quantization':'UnderlyingC may be within observedC +/-1second, covering nearest/floor/ceil to integer.',
      'necessary_condition':'Window sequenceA consists of oneextra window then sequenceB. Hence mA*mean(alphaA)-mB*mean(alphaB)=alpha_extra>=0.',
      'scope':'Rejects this fixed-window arithmetic-mean coefficient family only. Not recursive/adaptive weights depending on priorstate, different initialization windows, nonlinear aggregation, or arbitrarydirectC formulas.'}

def main():
    if '--spec' in sys.argv:
        (ROOT/'C_media_alpha_preregistro.json').write_text(json.dumps(SPEC,indent=2),encoding='utf-8')
        print(json.dumps({k:v for k,v in SPEC.items() if k!='lookbacks'},indent=2));return
    assert json.loads((ROOT/'C_media_alpha_preregistro.json').read_text())==SPEC
    cases=json.loads((ROOT/'C_matriz_frontera15s.json').read_text())['cases']
    a=next(c for c in cases if c['START']=='2026-10-12T19:03:15+00:00' and c['END']=='2026-10-12T19:23:45+00:00')
    b=next(c for c in cases if c['START']=='2026-10-12T19:03:30+00:00' and c['END']=='2026-10-12T19:23:45+00:00')
    assert a['OHLC'][1:]==b['OHLC']
    results=[]
    for L in SPEC['lookbacks']:
        windowsA=[a['OHLC'][i:i+L] for i in range(len(a['OHLC'])-L+1)]
        windowsB=[b['OHLC'][i:i+L] for i in range(len(b['OHLC'])-L+1)]
        assert windowsA[1:]==windowsB
        ma,mb=len(windowsA),len(windowsB)
        for scale in [24.,8.,72/27,72.,216.]:
            # Maximize the possible extraalpha using generous C bounds.
            alphaA_max=2/(1+scale*(round(a['C'])-1)/15)
            alphaB_min=2/(1+scale*(round(b['C'])+1)/15)
            extra_max=ma*alphaA_max-mb*alphaB_min
            results.append({'lookback':L,'scale':scale,'mA':ma,'mB':mb,
                            'maximum_extra_alpha_allowed_by_C_intervals':extra_max,
                            'impossible_nonnegative_extra_alpha':extra_max<0})
    out={'spec':SPEC,'pair':{'START_A':a['START'],'C_A':a['C'],'START_B':b['START'],'C_B':b['C'],'END':a['END']},
         'tested_configurations':len(results),'rejected':sum(r['impossible_nonnegative_extra_alpha'] for r in results),
         'results':results,'training32_used':False,'reserved_validation_used':False}
    (ROOT/'C_media_alpha_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'tested':len(results),'rejected':out['rejected'],
                      'least_negative_bound':max(r['maximum_extra_alpha_allowed_by_C_intervals'] for r in results),
                      'lookback20':[r for r in results if r['lookback']==20]},indent=2))

if __name__=='__main__':main()
