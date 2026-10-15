"""Conteo fijo23, deslizamiento local de START y END; curvas y OHLC auditados."""
import datetime,json
from analizar_C_fuente_vs_grafico import ROOT,read,fit_lite,COLS
from obtener_C import recover
def main():
    cases=[];failures=[]
    for minute,end_minute,cross in [(m,m+22,False)for m in [26,27,28,29,30]]+[(30,51,True),(29,52,True)]:
        prefix=f'C_23_cross_15{minute}_15{end_minute}' if cross else (f'C_23_shift_15{minute}' if minute!=28 else 'C_START_barrido_alcista_23');pair=['c','d']if minute!=28 or cross else ['e','f'];path=ROOT/'manual'/f'{prefix}_{pair[1]}.csv'
        if not path.exists():continue
        try:
            a,b=[read(f'{prefix}_{s}.csv')for s in pair];common=set(a)&set(b)
            assert common and all(a[t][k]==b[t][k]for t in common for k in COLS),'pareja inestable'
            start=int(datetime.datetime(2026,10,12,15,minute,tzinfo=datetime.timezone.utc).timestamp());ts=list(range(start,start+(end_minute-minute+1)*60,60));assert all(t in b for t in ts),'OHLC incompleto'
            fits=fit_lite(b,60,60);Cs=[v['C']for v in fits.values()];C=sum(Cs)/6;iv=recover(path)['C_seconds_interval']
            assert max(Cs)-min(Cs)<1e-7 and max(v['rmse']for v in fits.values())<1e-8,'Lite no familia'
            assert iv['lower_inclusive']-1e-8<=C<iv['upper_exclusive']+1e-8,'Character incompatible'
            rows=[{'time':t,**{k:float(b[t][k])for k in ['open','high','low','close']}}for t in ts]
            cases.append({'prefix':prefix,'pair':pair,'cross_control':cross,'reused_baseline':minute==28 and not cross,'START':datetime.datetime.fromtimestamp(start,datetime.timezone.utc).isoformat(),'END':datetime.datetime.fromtimestamp(ts[-1],datetime.timezone.utc).isoformat(),'bars':len(ts),'C':C,'prediction_local_count_only':None if cross else 81,'prediction_match':None if cross else abs(C-81)<1e-7,'high':max(r['high']for r in rows),'low':min(r['low']for r in rows),'Character_interval':iv,'repeated_curve_cells':len(common)*16,'OHLC':rows})
        except(ValueError,AssertionError,KeyError)as e:failures.append({'prefix':prefix,'error':str(e)})
    changes=[]
    for a,b in zip(cases,cases[1:]):
        ad={r['time']:r for r in a['OHLC']};bd={r['time']:r for r in b['OHLC']};shared=set(ad)&set(bd);assert all(ad[t]==bd[t]for t in shared)
        changes.append({'from':a['START'],'to':b['START'],'C_from':a['C'],'C_to':b['C'],'same_high':a['high']==b['high'],'same_low':a['low']==b['low'],'shared_OHLC_bars':len(shared),'removed':[ad[t]for t in sorted(set(ad)-set(bd))],'added':[bd[t]for t in sorted(set(bd)-set(ad))]})
    out={'cases':cases,'changes':changes,'failures':failures,'scope':'Four newly measured23bar windows plus repeated prior baseline and two crossed controls22/24bars, native60s. No general C formula.'}
    (ROOT/'C_23_desplazamientos.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'cases':[{k:v for k,v in c.items()if k!='OHLC'}for c in cases],'changes':changes,'failures':failures},indent=2))
if __name__=='__main__':main()
