"""Audita entrega v4 congelada: datos, generador y Pine real vs emulador declarado.

No ejecuta imports/código superior de los archivos externos ni los modifica.
"""
import ast,json,math,hashlib,re
from pathlib import Path
from analizar_C_fuente_vs_grafico import ROOT
from auditar_Gemini_v31 import metrics

SOURCE=Path(r'C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27')
FILES={'reports/Gemini_v4_informe_recibido.md':SOURCE/'INFORME_DESCUBRIMIENTO_ORIGEN_C.md',
       'Gemini_v4_evaluador_recibido.py':SOURCE/'scratch/evaluate_unified_model_v4.py',
       'pine/Gemini_v4_recibido.pine':SOURCE/'scratch/PoiSzn_C_Deterministic_Lab_v4.pine',
       'Gemini_v4_equivalencia_recibida.py':SOURCE/'scratch/verify_py_pine_equiv.py',
       'Gemini_v4_cases112_recibidos.json':SOURCE/'scratch/cases_112.json'}

def extract_function(filename,name):
    tree=ast.parse((ROOT/filename).read_text(encoding='utf-8-sig'))
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    env={'math':math}
    exec(compile(ast.Module(body=[node],type_ignores=[]),'frozen_function_only','exec'),env)
    return env[name]

def translate_pine_engine():
    text=(ROOT/'pine/Gemini_v4_recibido.pine').read_text(encoding='utf-8-sig')
    engine=text.split('// --- 3. MOTOR DETERMINISTA DE C ---')[1].split('float C_final')[0]
    body=engine.split('if is_end_bar\n',1)[1]
    pre='''def actual_pine_C(c):
    rows=c['OHLC']; bar_cnt=c['bars']; dt=c['dt']
    rng_high=max(r['high'] for r in rows); rng_low=min(r['low'] for r in rows)
    start_open=rows[0]['open']; close=rows[-1]['close']; open=rows[-1]['open']
    high=rows[-1]['high']; prev_high=rows[-2]['high'] if len(rows)>1 else high
'''
    lines=[]
    for line in body.splitlines():
        if not line.strip() or line.lstrip().startswith('//'):continue
        indent=len(line)-len(line.lstrip());s=line.strip()
        s=re.sub(r'^(float|bool|string|int)\s+','',s).replace(':=','=').replace('math.max','max').replace('high[1]','prev_high')
        if s.startswith('else if '):s='elif '+s[8:]+':'
        elif s.startswith('if '):s+=':'
        elif s=='else':s+=':'
        elif '?' in s:
            lhs,expr=s.split('=',1);cond,values=expr.split('?',1);yes,no=values.split(':',1)
            s=lhs+'= ('+yes.strip()+' if '+cond.strip()+' else '+no.strip()+')'
        lines.append(' '*indent+s)
    code=pre+'\n'.join(lines)+'\n    return c_auto\n'
    ast.parse(code)
    (ROOT/'Gemini_v4_motor_Pine_traducido.py').write_text(code,encoding='utf-8')
    env={'math':math};exec(compile(code,'translated_actual_Pine_scalar_engine','exec'),env)
    return env['actual_pine_C']

def key(c):return (c['dt'],c['OHLC'][0]['time'],c['OHLC'][-1]['time'])

def independently_build112():
    master=json.loads((ROOT/'C_dataset_verificado.json').read_text())['cases']
    original=[dict(c,partition=c['split']) for c in master]
    pred=json.loads((ROOT/'C_evolucion87_predicciones.json').read_text());res=json.loads((ROOT/'C_evolucion87_resultados.json').read_text())
    original += [{'id':f'oct13_{c["END"][11:16]}','START':'2026-10-13T06:25:00+00:00','END':c['END'],
                  'bars':c['bars'],'dt':60,'C':c['C'],'OHLC':pred['OHLC'][:c['bars']],'partition':'oct13_existing'} for c in res['cases']]
    extra=[]
    for tag in ['replica24','rama24_resolucion','transicion1923','prefijo192345','recorte1903']:
        predictions=json.loads((ROOT/f'C_{tag}_predicciones.json').read_text())['cases']
        results=json.loads((ROOT/f'C_{tag}_resultados.json').read_text())['cases'];byid={c['id']:c for c in predictions}
        for r in results:
            c=byid[r['id']];extra.append({'id':c['id'],'START':c['START'],'END':c['END'],'bars':c.get('bars',len(c['OHLC'])),
                                         'dt':c.get('dt',60),'C':r['C'],'OHLC':c['OHLC'],'partition':'additional_controls'})
    return original+extra

def main():
    hashes={}
    for name,path in FILES.items():
        raw=path.read_bytes();(ROOT/name).write_bytes(raw);hashes[name]=hashlib.sha256(raw).hexdigest()
    predict=extract_function('Gemini_v4_evaluador_recibido.py','predict_C')
    claimed_pine=extract_function('Gemini_v4_equivalencia_recibida.py','pine_C')
    actual_pine=translate_pine_engine()
    supplied=json.loads((ROOT/'Gemini_v4_cases112_recibidos.json').read_text());independent=independently_build112()
    assert len(supplied)==len(independent)==112
    bykey={key(c):c for c in independent};assert len(bykey)==112
    assert len({key(c) for c in supplied})==112
    for c in supplied:
        v=bykey[key(c)];assert c['OHLC']==v['OHLC'] and abs(c['C']-v['C'])<1e-7 and c['bars']==v['bars'],c['id']
        assert c['partition']==v['partition'],c['id']
    rows=[]
    for c in independent:
        pred,branch=predict(c);pine=actual_pine(c);declared=claimed_pine(c)
        rows.append({k:v for k,v in c.items() if k!='OHLC'}|{'python_prediction':pred,'python_branch':branch,
                      'actual_pine_prediction':pine,'declared_emulator_prediction':declared})
    summaries={part:{'all':metrics([r for r in rows if r['partition']==part]),
                     'long_only':metrics([r for r in rows if r['partition']==part and r['bars']>=21])}
               for part in ['training','validation','oct13_existing','additional_controls']}
    summaries['total112']=metrics(rows);summaries['total_long']=metrics([r for r in rows if r['bars']>=21])
    matrix=json.loads((ROOT/'C_matriz_frontera15s.json').read_text())['cases'];matrix_rows=[];new_rows=[]
    for c in matrix:
        pred,branch=predict(c);row={k:v for k,v in c.items() if k not in ['OHLC','state','provenance']}|{'id':f'{c["START"]}_{c["END"]}',
                       'python_prediction':pred,'python_branch':branch,'actual_pine_prediction':actual_pine(c),'already_in112':key(c) in bykey}
        matrix_rows.append(row)
        if key(c) not in bykey:new_rows.append(row)
    # Deterministic artificial input exposes non-equivalence of their emulator,
    # without claiming this invented window is an observed original-indicator case.
    synthetic={'bars':21,'dt':60,'OHLC':[{'open':124.,'high':125.,'low':100.,'close':120.}]*20+
               [{'open':120.,'high':135.,'low':119.,'close':127.}]}
    artificial={'OHLC':synthetic['OHLC'],'Python':predict(synthetic)[0],'actual_Pine':actual_pine(synthetic),'declared_emulator':claimed_pine(synthetic),
                'scope':'Invented logical counterexample, no referenceC; not accuracy validation.'}
    out={'scope':'Audit frozen externalv4 without fitting. All112data checked against independent local sources. Validation explicitly scored to audit external model; not blind/prospective. Matrix extras already measured/available, no claim unseen by Gemini.',
         'hashes':hashes,'source112_verified':True,'summary':summaries,
         'actual_Python_Pine_differences112':[r for r in rows if abs(r['python_prediction']-r['actual_pine_prediction'])>1e-7],
         'declared_emulator_differences112':[r for r in rows if abs(r['actual_pine_prediction']-r['declared_emulator_prediction'])>1e-7],
         'matrix9':{'metrics':metrics(matrix_rows),'rows':matrix_rows},'outside112_matrix':{'metrics':metrics(new_rows),'rows':new_rows},
         'artificial_emulator_counterexample':artificial,'rows112':rows}
    (ROOT/'Gemini_v4_auditoria.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'summary':summaries,'actualPyPine112differences':len(out['actual_Python_Pine_differences112']),
                      'declared_emulator_differences112':len(out['declared_emulator_differences112']),
                      'matrix9':out['matrix9'],'outside112':out['outside112_matrix'],
                      'artificial_counterexample':{k:v for k,v in artificial.items() if k!='OHLC'}},indent=2))

if __name__=='__main__':main()
