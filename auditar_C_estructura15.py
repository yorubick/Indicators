"""Réplica15s: END:45 inferido por reconstrucción, agregación exacta y pares."""
import hashlib,json,traceback
from datetime import datetime,timezone
from pathlib import Path
from analizar_C_frontera_1s import read
from analizar_C_fuente_vs_grafico import fit_lite,LANES
from analizar_C_bordes26 import stamp
from analizar_C_traslacion50 import comparison
from auditar_C_estructura import history_check

ROOT=Path(__file__).parent
BASES=dict(zip(LANES,[24,89/3,8,89/9,72/27,89/27]))

def main():
    spec=json.loads((ROOT/'C_ESTRUCTURA_15S_PREREGISTRO.json').read_text())
    cases=json.loads((ROOT/'C_ANCLAS_ESTRUCTURA_PREREGISTRO.json').read_text())['measurement_cases']
    cases+=json.loads((ROOT/'C_ANCLAS_ESTRUCTURA_CORRECCION_1907.json').read_text())['registered_before_new_measurements']
    old={r['id']:r for r in json.loads((ROOT/'C_estructura_resultados.json').read_text())['results']}
    results=[];hashes={};failures=[];repeat_history=[]
    repair=json.loads((ROOT/'C_ESTRUCTURA15_REPETICION_A_FIRST_START_PLUS.json').read_text())
    for case in cases:
        try:
            s,minute_end=stamp(case['START']),stamp(case['END']);e=minute_end+45
            suffixes=repair['new_exports'] if case['id']==repair['case'] else ['a','b']
            paths=[ROOT/'manual'/f'C_estructura15_{case["id"]}_{suffix}.csv' for suffix in suffixes]
            a,b=[read(p) for p in paths];repeat=comparison(a,b)
            if case['id']==repair['case']:
                original_paths=[ROOT/'manual'/f'C_estructura15_{case["id"]}_{suffix}.csv' for suffix in ['a','b']]
                original_a,original_b=[read(p) for p in original_paths]
                original_cs={suffix:sum(v['C'] for v in fit_lite(rows,15,15).values())/6 for suffix,rows in [('a',original_a),('b',original_b)]}
                try:
                    comparison(original_a,original_b)
                    original_status='passed'
                except AssertionError:
                    original_status='failed; preserved, superseded by preregistered c/d repetition'
                repeat_history.append({'id':case['id'],'original_pair_status':original_status,'original_C':original_cs,
                                       'original_b_vs_new_d':comparison(original_b,b),'registered_repetition':repair})
                hashes.update({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in original_paths})
            window=list(range(s,e+1,15));assert len(window)==4*old[case['id']]['n']
            assert all(t in b for t in range(s,e+3601,15)),'missing native quarter-bars'
            native=read(ROOT/'manual'/f'C_estructura_{case["id"]}_b.csv')
            aggregation_errors=[]
            for t in range(s,minute_end+3601,60):
                q=[b[t+j] for j in [0,15,30,45]]
                agg={'open':float(q[0]['open']),'high':max(float(r['high']) for r in q),'low':min(float(r['low']) for r in q),
                     'close':float(q[-1]['close']),'Volume':sum(float(r['Volume']) for r in q)}
                for k,v in agg.items():
                    if v!=float(native[t][k]):aggregation_errors.append({'time':t,'column':k,'aggregate':v,'original':float(native[t][k])})
            assert not aggregation_errors,('aggregation mismatch',aggregation_errors[:3])
            fits=fit_lite(b,15,15);cs=[v['C'] for v in fits.values()];C=sum(cs)/6
            assert max(cs)-min(cs)<1e-6 and max(v['rmse'] for v in fits.values())<1e-8
            hi=max(float(b[t]['high']) for t in window);lo=min(float(b[t]['low']) for t in window)
            assert hi==old[case['id']]['H'] and lo==old[case['id']]['L']
            rupture=next(t for t in range(e+15,e+3601,15) if float(b[t]['close'])>hi or float(b[t]['close'])<lo)
            bull=float(b[rupture]['close'])>hi;seed=float(b[e]['low' if bull else 'high']);values=dict.fromkeys(LANES,seed)
            errs=[];vis=0
            for t in range(e+15,e+3601,15):
                for lane,base in BASES.items():
                    values[lane]+=2/(base*C/15+1)*(float(b[t]['close'])-values[lane])
                    vis+=bool(b[t][lane])!=(t>=rupture)
                    if b[t][lane]:errs.append(abs(values[lane]-float(b[t][lane])))
            assert vis==0 and max(errs)<1e-8,('unexpected END,seed or recurrence',vis,max(errs))
            short=max(15,len(window)*15*10/183) if len(window)<21 else None
            if short is not None:assert abs(C-short)<1e-6
            results.append({**case,'START_15s':datetime.fromtimestamp(s,timezone.utc).isoformat(),'END_15s':datetime.fromtimestamp(e,timezone.utc).isoformat(),
                            'n15':len(window),'n60':old[case['id']]['n'],'C15':C,'C60':old[case['id']]['C'],
                            'C15_div_source':C/15,'C60_div_source':old[case['id']]['C']/60,'H':hi,'L':lo,
                            'rupture15_UTC':datetime.fromtimestamp(rupture,timezone.utc).isoformat(),'rupture60_UTC':old[case['id']]['rupture_UTC'],
                            'seed15':seed,'short_rule_prediction':short,'reconstruction_max_error':max(errs),'visibility_errors':vis,
                            'aggregation_mismatches':aggregation_errors,'repeat_common_bars':repeat['common_closed_bars'],'exports':[p.name for p in paths],'fits':fits})
            hashes.update({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
        except Exception as ex:
            failures.append({'id':case['id'],'reason':repr(ex),'traceback':traceback.format_exc()})
    ret=read(ROOT/'manual/C_estructura15_regreso_1m_final.csv')
    assert all(t in ret for t in range(stamp('18:55'),stamp('19:20')+3601,60))
    baseline=read(ROOT/'manual/C_estructura_regreso_final.csv')
    back=comparison(baseline,ret)
    retfits=fit_lite(ret,60,60);assert all(abs(v['C']-62)<1e-6 for v in retfits.values())
    out={'preregistered':spec,'results':results,'failures':failures,'repeat_history':repeat_history,'sha256':hashes,'return_check':back,'return_fits':retfits,
         'limitations':'Sampling/source and branch change together; preserved minute OHLCV and event labels do not preserve intrabar close-path, first rupture or selected END seed.'}
    (ROOT/'C_estructura15_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'table':[{k:r[k] for k in ['id','n15','C15','C60','rupture15_UTC']} for r in results],
                      'failures':failures,'return_verified':True},indent=2))

if __name__=='__main__':main()
