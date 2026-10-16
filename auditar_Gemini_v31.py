"""Reproduce métricas de un modelo congelado y contrasta su Pine.

Extrae solo predict_C del evaluador; no ejecuta su código superior.
No ajusta coeficientes. La particiónvalidation se puntúa explícitamente
para auditar este modelo externo: no queda como prueba ciega para él.
"""
import ast,json,math,hashlib
import numpy as np
from analizar_C_fuente_vs_grafico import ROOT

def pine_C(c):
    n,dt,r=c['bars'],c['dt'],c['OHLC']
    if n<21:return max(dt,n*dt*10/183)
    if dt==15:return 16.0
    if dt==120:return 137.0
    H=max(x['high'] for x in r);L=min(x['low'] for x in r);R=H-L
    pos=(r[0]['open']-L)/R if R else .5;bull=r[-1]['close']>r[0]['open']
    if 21<=R<=22 and pos>=.35:return math.floor((n-1)*dt/24)
    if n==25 and R<=24.75 and r[-1]['high']==H:return 60.
    if 22<R<=26 and pos>=.35 and bull and n<=24:return 71.
    if 25<=R<=28.5 and pos>=.30 and n>=25:return 128. if n==25 else 134. if n==26 else 109.
    if R>95 and n==23:return 83.
    if R>95 and n==24:return 76.
    if n==22 and R==24.5 and pos<.20:return 102.
    if 86<=R<=88 and n==25:return 93.
    if R>95:return 62.
    if R>65:return 68. if pos<=.16 or (n<=22 and pos<=.25) else 75. if pos<=.25 else 82.
    if 28<=R<=40 and pos>.55:return 84.
    if 32<=R<=38:return 78.
    if R<=24.5 and not bull:return 75.
    return 77.

def metrics(rows,key='python_prediction'):
    errors=[abs(r[key]-r['C']) for r in rows]
    return {'cases':len(rows),'exact_tol_1e_7':sum(e<1e-7 for e in errors),
            'within3':sum(e<=3+1e-7 for e in errors),'within5':sum(e<=5+1e-7 for e in errors),
            'MAE_full_precision':sum(errors)/len(errors),
            'MAE_rounded_errors_like_Gemini':sum(round(e,2) for e in errors)/len(errors)}

def main():
    source=(ROOT/'Gemini_v31_evaluador_recibido.py').read_text(encoding='utf-8-sig')
    tree=ast.parse(source);function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='predict_C')
    env={'np':np};exec(compile(ast.Module(body=[function],type_ignores=[]),'frozen_Gemini_predict_C','exec'),env)
    predict=env['predict_C'];master=json.loads((ROOT/'C_dataset_verificado.json').read_text())['cases']
    pred13=json.loads((ROOT/'C_evolucion87_predicciones.json').read_text());res13=json.loads((ROOT/'C_evolucion87_resultados.json').read_text())
    original=[dict(c,partition=c['split']) for c in master]
    original += [{'id':f'oct13_{c["END"][11:16]}','START':'2026-10-13T06:25:00+00:00',
                  'END':c['END'],'bars':c['bars'],'dt':60,'C':c['C'],
                  'OHLC':pred13['OHLC'][:c['bars']],'partition':'oct13_existing'} for c in res13['cases']]
    new=[]
    for tag in ['replica24','rama24_resolucion','transicion1923','prefijo192345','recorte1903']:
        preds=json.loads((ROOT/f'C_{tag}_predicciones.json').read_text())['cases']
        results=json.loads((ROOT/f'C_{tag}_resultados.json').read_text())['cases']
        by_id={c['id']:c for c in preds}
        for r in results:
            c=by_id[r['id']]
            new.append({'id':c['id'],'START':c['START'],'END':c['END'],
                        'bars':c.get('bars',len(c['OHLC'])),'dt':c.get('dt',60),
                        'C':r['C'],'OHLC':c['OHLC'],'partition':'additional_controls'})
    rows=[]
    for c in original+new:
        val,branch=predict(c)
        rows.append({k:v for k,v in c.items() if k!='OHLC'}|{'python_prediction':float(val),'python_branch':branch,
                     'pine_prediction':pine_C(c),'original_Gemini_exact':abs(val-c['C'])<1e-5 or round(val)==round(c['C'])})
    oldrows=rows[:len(original)];newrows=rows[len(original):]
    summary={}
    for partition in ['training','validation','oct13_existing']:
        subset=[r for r in oldrows if r['partition']==partition]
        summary[partition]={'all':metrics(subset),'long_only':metrics([r for r in subset if r['bars']>=21])}
    summary['original99']=metrics(oldrows)
    summary['additional_controls']=metrics(newrows)
    summary['additional15s']=metrics([r for r in newrows if r['dt']==15])
    mismatches=[r for r in oldrows if abs(r['python_prediction']-r['pine_prediction'])>1e-7]
    out={'scope':'Frozen external model; no training/fitting. Explicit scoring of originalvalidation for audit, not blind validation. Additional controls already measured and available to Gemini; not certified unseen/prospective for its development.',
         'snapshot_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['Gemini_v31_evaluador_recibido.py','pine/Gemini_v31_recibido.pine']},
         'summary':summary,'Python_Pine_original99_differences':mismatches,'rows':rows}
    (ROOT/'Gemini_v31_auditoria.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'summary':summary,'Python_Pine_different_predictions':len(mismatches),
                      'differences':[{k:r[k] for k in ['id','C','python_prediction','pine_prediction']} for r in mismatches],
                      'additional_controls':[{k:r[k] for k in ['id','dt','C','python_prediction']} for r in newrows]},indent=2))

if __name__=='__main__':main()
