"""Puntúa extrapolaciones locales sin cambiar coeficientes tras medir."""
import json
from analizar_C_fuente_vs_grafico import ROOT,read,fit_lite,COLS
from obtener_C import recover
def main():
    p=json.loads((ROOT/'C_evolucion87_predicciones.json').read_text());cases=[];failures=[]
    for prediction in p['predictions']:
        minute=prediction['END'][14:16];prefix='C_noevent_2_'+('before'if minute=='45'else'after')if minute in ['45','46']else'C_evolucion87_END06'+minute;pair=['e','f']if(ROOT/'manual'/f'{prefix}_f.csv').exists()else['c','d']
        try:
            a,b=[read(f'{prefix}_{s}.csv')for s in pair];common=set(a)&set(b);assert common and all(a[t][k]==b[t][k]for t in common for k in COLS),'pareja inestable'
            bars=p['OHLC'][:prediction['bars']]
            assert all(r['time']in b and all(float(b[r['time']][k])==r[k]for k in ['open','high','low','close'])for r in bars),'OHLC distinto preregistro'
            fits=fit_lite(b,60,60);Cs=[v['C']for v in fits.values()];C=sum(Cs)/6;iv=recover(ROOT/'manual'/f'{prefix}_{pair[1]}.csv')['C_seconds_interval']
            assert max(Cs)-min(Cs)<1e-7 and max(v['rmse']for v in fits.values())<1e-8,'Lite no familia'
            assert iv['lower_inclusive']-1e-8<=C<iv['upper_exclusive']+1e-8,'Character incompatible'
            row={**prediction,'prefix':prefix,'pair':pair,'C':C,'calibration_case':minute in ['45','46'],'age_model_matches':{k:abs(v-C)<1e-7 for k,v in prediction['age_model_predictions'].items()},'linear_count_match':abs(C-prediction['linear_count_prediction'])<1e-7,'Character_interval':iv,'repeat_cells':len(common)*16}
            if cases:
                delta=C-cases[-1]['C'];row['delta_C']=delta;row['Gemini_pullback_match']=(20-1e-7<=delta<=57+1e-7)if prediction['pullback_definition']['countertrend_body']else None
            cases.append(row)
        except(ValueError,AssertionError,KeyError)as e:failures.append({'prefix':prefix,'error':str(e)})
    fresh=[c for c in cases if not c['calibration_case']];summary={'new_cases':len(fresh),'age_model_new_matches':{k:sum(c['age_model_matches'][k]for c in fresh)for k in p['age_model_intercepts']},'linear_new_matches':sum(c['linear_count_match']for c in fresh),'new_pullback_test_cases':sum(c.get('Gemini_pullback_match')is not None for c in fresh),'new_pullback_matches':sum(c.get('Gemini_pullback_match')is True for c in fresh)}
    out={'cases':cases,'summary':summary,'failures':failures,'scope':'Known87/84 used only to calibrate localage/count slope-3; subsequent fourC measured after frozen predictions. Finite local hypotheses, not general generator. Trend defined from priorclose minus STARTclose; ENDcolor from close-open.'};(ROOT/'C_evolucion87_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps({'summary':summary,'cases':[{k:c[k]for k in ['END','C','age_model_predictions','events','pullback_definition'] }for c in cases],'failures':failures},indent=2))
if __name__=='__main__':main()
