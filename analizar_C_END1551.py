"""END15:51 fijo, START26..31; prefijos y conteo evaluados sin inferir código privado."""
import datetime,json
from analizar_C_fuente_vs_grafico import ROOT,read,fit_lite,COLS
from obtener_C import recover
def main():
    cases=[];failures=[]
    for minute,end_minute in [(m,51)for m in range(26,32)]+[(27,52),(28,52)]:
        prefix=('C_23_shift_1529' if minute==29 else 'C_23_cross_1530_1551') if end_minute==51 and minute in [29,30] else f'C_END15{end_minute}_START_15{minute}'
        pair=['e','f'] if (ROOT/'manual'/f'{prefix}_f.csv').exists() else ['c','d'];path=ROOT/'manual'/f'{prefix}_{pair[1]}.csv'
        try:
            a,b=[read(f'{prefix}_{s}.csv')for s in pair];common=set(a)&set(b)
            assert common and all(a[t][k]==b[t][k]for t in common for k in COLS),'pareja inestable'
            start=int(datetime.datetime(2026,10,12,15,minute,tzinfo=datetime.timezone.utc).timestamp());ts=list(range(start,start+(end_minute-minute+1)*60,60));assert all(t in b for t in ts),'OHLC incompleto'
            fits=fit_lite(b,60,60);Cs=[v['C']for v in fits.values()];C=sum(Cs)/6;iv=recover(path)['C_seconds_interval']
            assert max(Cs)-min(Cs)<1e-7 and max(v['rmse']for v in fits.values())<1e-8,'Lite no familia'
            assert iv['lower_inclusive']-1e-8<=C<iv['upper_exclusive']+1e-8,'Character incompatible'
            rows=[{'time':t,**{k:float(b[t][k])for k in ['open','high','low','close']}}for t in ts];pred=({27:93,28:75}[minute] if end_minute==52 else (75 if minute<=28 else None))
            cases.append({'prefix':prefix,'pair':pair,'reused':end_minute==51 and minute in [29,30],'START':datetime.datetime.fromtimestamp(start,datetime.timezone.utc).isoformat(),'END':datetime.datetime.fromtimestamp(ts[-1],datetime.timezone.utc).isoformat(),'bars':len(ts),'C':C,'prediction_before_measurement':pred,'prediction_kind':'END52_continuity' if end_minute==52 else 'prefix_irrelevant','prediction_match':abs(C-pred)<1e-7 if pred is not None else None,'high':max(r['high']for r in rows),'low':min(r['low']for r in rows),'Character_interval':iv,'repeated_curve_cells':len(common)*16,'OHLC':rows})
        except (ValueError,AssertionError,KeyError)as e:failures.append({'prefix':prefix,'error':str(e)})
    transitions=[]
    fixed=[c for c in cases if c['END'][11:16]=='15:51']
    for a,b in zip(fixed,fixed[1:]):
        am={r['time']:r for r in a['OHLC']};bm={r['time']:r for r in b['OHLC']};common=set(am)&set(bm);assert all(am[t]==bm[t]for t in common)
        transitions.append({'from':a['START'],'to':b['START'],'C_from':a['C'],'C_to':b['C'],'same_global_extrema':a['high']==b['high'] and a['low']==b['low'],'removed':[am[t]for t in sorted(set(am)-set(bm))],'shared_OHLC_bars':len(common)})
    out={'cases':cases,'transitions':transitions,'failures':failures,'scope':'Six new selections, two prior controls, independent repeat of93; native1m. General C formula unknown.'}
    (ROOT/'C_END1551.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'cases':[{k:v for k,v in c.items()if k!='OHLC'}for c in cases],'transitions':transitions,'failures':failures},indent=2))
if __name__=='__main__':main()
