"""Audita cajas estructurales registradas, interpretaciones y controles de borde."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
from analizar_C_frontera_1s import read
from analizar_C_fuente_vs_grafico import fit_lite,LANES
from analizar_C_bordes26 import stamp
from analizar_C_traslacion50 import comparison

ROOT=Path(__file__).parent
BASES=dict(zip(LANES,[24,89/3,8,89/9,72/27,89/27]))

def history_check(a,b,cutoff):
    common=set(a)&set(b)
    assert common
    for t in common:
        assert all(a[t][k]==b[t][k] for k in ['open','high','low','close'])
    differences=[{'time':datetime.fromtimestamp(t,timezone.utc).isoformat(),'old':a[t]['Volume'],'new':b[t]['Volume']} for t in sorted(common) if a[t]['Volume']!=b[t]['Volume']]
    assert all(t>cutoff or a[t]['Volume']==b[t]['Volume'] for t in common)
    return {'common_bars':len(common),'full_OHLC_equal':True,'full_OHLCV_equal':not differences,'volume_differences':differences,
            'OHLCV_equal_through_experiment_horizon':True,'horizon_UTC':datetime.fromtimestamp(cutoff,timezone.utc).isoformat(),
            'scope_note':'Horizon was preregistered; global volume mismatch remains a failed control, not erased. Scoped interpretation made after detecting it.'}

def main():
    original=json.loads((ROOT/'C_ANCLAS_ESTRUCTURA_PREREGISTRO.json').read_text())
    correction=json.loads((ROOT/'C_ANCLAS_ESTRUCTURA_CORRECCION_1907.json').read_text())
    cases=original['measurement_cases']+correction['registered_before_new_measurements']
    source=read(ROOT/'manual/C_startSweep1920_geometria_historia_larga.csv')
    # Verify earliest pivot correction from price alone.
    assert float(source[stamp('19:07')]['low'])<min(float(source[stamp('19:06')]['low']),float(source[stamp('19:08')]['low']))
    results=[];hashes={}
    for case in cases:
        s,e=stamp(case['START']),stamp(case['END']);window=list(range(s,e+1,60))
        paths=[ROOT/'manual'/f'C_estructura_{case["id"]}_{suffix}.csv' for suffix in ['a','b']]
        a,b=[read(p) for p in paths];repeat=comparison(a,b)
        common=set(source)&set(b)
        native_check=history_check(source,b,e+3600)
        assert all(t in b for t in window) and all(t in b for t in range(e+60,e+3660,60))
        fits=fit_lite(b,60,60);cs=[v['C'] for v in fits.values()];C=sum(cs)/6
        assert max(cs)-min(cs)<1e-6 and max(v['rmse'] for v in fits.values())<1e-8
        hi=max(float(b[t]['high']) for t in window);lo=min(float(b[t]['low']) for t in window)
        rupture=next(t for t in range(e+60,e+3660,60) if float(b[t]['close'])>hi or float(b[t]['close'])<lo)
        bull=float(b[rupture]['close'])>hi;seed=float(b[e]['low' if bull else 'high']);values=dict.fromkeys(LANES,seed)
        errs=[];vis=0
        for t in range(e+60,e+3660,60):
            for lane,base in BASES.items():
                values[lane]+=2/(base*C/60+1)*(float(b[t]['close'])-values[lane])
                vis+=bool(b[t][lane])!=(t>=rupture)
                if b[t][lane]:errs.append(abs(values[lane]-float(b[t][lane])))
        assert vis==0 and max(errs)<1e-8
        short=max(60,len(window)*60*10/183) if len(window)<21 else None
        if short is not None:assert abs(C-short)<1e-6
        results.append({**case,'n':len(window),'duration_elapsed_seconds':e-s,'C':C,'H':hi,'L':lo,
                        'rupture_UTC':datetime.fromtimestamp(rupture,timezone.utc).isoformat(),'direction':'bull' if bull else 'bear','seed':seed,
                        'previous_short_rule_prediction':short,'repeat_common_bars':repeat['common_closed_bars'],'native_common_bars':len(common),
                        'reconstruction_max_error':max(errs),'visibility_errors':vis,'fits':fits,'native_check':native_check})
        hashes.update({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    retpath=ROOT/'manual/C_estructura_regreso_final.csv';ret=read(retpath)
    baseline=read(ROOT/'manual/C_simetria1855_base.csv')
    back=history_check(baseline,ret,stamp('19:20')+3600)
    common=set(baseline)&set(ret)
    assert all(baseline[t][k]==ret[t][k] for t in common for k in LANES)
    back['all_six_Lite_curves_equal']=True
    assert all(abs(v['C']-62)<1e-6 for v in fit_lite(ret,60,60).values())
    hashes[retpath.name]=hashlib.sha256(retpath.read_bytes()).hexdigest()
    out={'protocol':original,'correction':correction,'results':results,'return_check':back,'sha256':hashes,
         'interpretation':'All short cases match existing rule, no new generator information. Last mitigation candidate has C62 with four neighbors134,107,109,125. Structural selection operational and provisional; no predictive law demonstrated.'}
    (ROOT/'C_estructura_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'table':[{k:r[k] for k in ['id','START','END','n','C','H','L','rupture_UTC']} for r in results],
                      'within_range_and_hour_controls_passed':True,'global_volume_control_passed':all(r['native_check']['full_OHLCV_equal'] for r in results)},indent=2))

if __name__=='__main__':main()
