"""Puntúa predicciones registradas antes de observar los dos pares nuevos de C."""
import json
from analizar_C_fuente_vs_grafico import ROOT,read,fit_lite,COLS
from obtener_C import recover
from lab_base_C import states
def main():
    predictions=json.loads((ROOT/'C_sin_evento_predicciones.json').read_text());results=[];failures=[]
    for pred in predictions['cases']:
        measured=[]
        try:
            for stage,n in [('before',21),('after',22)]:
                prefix='C_'+pred['id']+'_'+stage;pair=['e','f']if (ROOT/'manual'/f'{prefix}_f.csv').exists()else ['c','d'];a,b=[read(f'{prefix}_{s}.csv')for s in pair];common=set(a)&set(b)
                assert common and all(a[t][k]==b[t][k]for t in common for k in COLS),'pareja inestable'
                for r in pred['OHLC'][:n]:assert r['time']in b and all(float(b[r['time']][k])==r[k]for k in ['open','high','low','close']),'OHLC distinto predicción'
                fits=fit_lite(b,60,60);Cs=[v['C']for v in fits.values()];C=sum(Cs)/6;iv=recover(ROOT/'manual'/f'{prefix}_{pair[1]}.csv')['C_seconds_interval']
                assert max(Cs)-min(Cs)<1e-7 and max(v['rmse']for v in fits.values())<1e-8,'Lite no familia'
                assert iv['lower_inclusive']-1e-8<=C<iv['upper_exclusive']+1e-8,'Character incompatible'
                measured.append({'prefix':prefix,'pair':pair,'C':C,'bars':n,'Character_interval':iv,'repeat_cells':len(common)*16})
            hist=list(states(pred['OHLC']));a,b=hist[-2:];events={'newH':b['new_high'],'newL':b['new_low'],'pivotH':a['last_confirmed_high']!=b['last_confirmed_high'],'pivotL':a['last_confirmed_low']!=b['last_confirmed_low']};assert not any(events.values())and events==pred['events']
            delta=measured[1]['C']-measured[0]['C'];results.append({'id':pred['id'],'START':pred['START'],'END_before':pred['END_before'],'END_after':pred['END_after'],'predicted_delta_C':pred['prediction_delta_C'],'measured_delta_C':delta,'prediction_match':abs(delta)<1e-7,'events':events,'same_global_extrema':a['high']==b['high']and a['low']==b['low'],'measured':measured,'OHLC':pred['OHLC']})
        except(ValueError,AssertionError,KeyError)as e:failures.append({'id':pred['id'],'error':str(e)})
    out={'cases':results,'failures':failures,'scope':'Two prospective disjoint13oct ranges chosen from OHLC before C measurements; tests defined event-only change hypothesis, not a complete formula. Existing validation27 untouched.'};(ROOT/'C_sin_evento_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps({**{k:v for k,v in out.items()if k!='cases'},'cases':[{k:v for k,v in c.items()if k!='OHLC'}for c in results]},indent=2))
if __name__=='__main__':main()
