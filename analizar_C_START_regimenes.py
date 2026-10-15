"""END fijo: prefijos adicionales y eliminación de primeras velas en dos regímenes."""
import json,datetime
from analizar_C_fuente_vs_grafico import ROOT,read,fit_lite,COLS
from obtener_C import recover
def main():
    bases=json.loads((ROOT/'C_21_regimenes.json').read_text())['cases'];cases=[];failures=[]
    for tag,base in zip(['alcista','lateral'],bases):
        end=int(datetime.datetime.fromisoformat(base['END']).timestamp());baseline={int(r['time']):r for r in base['OHLC']}
        for n in [18,19,20,22,23,24]:
            prefix=f'C_START_barrido_{tag}_{n}';pair=['e','f'] if (ROOT/'manual'/f'{prefix}_f.csv').exists() else ['c','d'];path=ROOT/'manual'/f'{prefix}_{pair[1]}.csv'
            if not path.exists():continue
            try:
                a,b=[read(f'{prefix}_{s}.csv')for s in pair];common=set(a)&set(b)
                assert common and all(a[t][k]==b[t][k]for t in common for k in COLS),'pareja inestable'
                ts=list(range(end-(n-1)*60,end+1,60));assert all(t in b for t in ts),'OHLC incompleto'
                fits=fit_lite(b,60,60);Cs=[v['C']for v in fits.values()];C=sum(Cs)/6;ct=recover(path);iv=ct['C_seconds_interval']
                assert max(Cs)-min(Cs)<1e-7 and max(v['rmse']for v in fits.values())<1e-8,'Lite no familia'
                assert iv['lower_inclusive']-1e-8<=C<iv['upper_exclusive']+1e-8,'Character incompatible'
                selected=[{'time':t,**{k:float(b[t][k])for k in ['open','high','low','close']}}for t in ts]
                hi=max(r['high']for r in selected);lo=min(r['low']for r in selected)
                unchanged=all(all(float(b[t][k])==r[k]for k in ['open','high','low','close'])for t,r in baseline.items()) if n>21 else None
                if n>21:assert unchanged,'sufijo21 cambiado'
                pred=max(60,n*600/183) if n<21 else base['C']
                cases.append({'prefix':prefix,'pair':pair,'regime':tag,'START':datetime.datetime.fromtimestamp(ts[0],datetime.timezone.utc).isoformat(),'END':base['END'],'bars':n,'C':C,'baseline_21_C':base['C'],'prediction_before_measurement':pred,'prediction_kind':'short_rule' if n<21 else 'last21_only','prediction_match':abs(C-pred)<1e-7,'high':hi,'low':lo,'same_global_extrema_as21':hi==base['high'] and lo==base['low'],'same_last21_OHLC':unchanged,'Character_interval':iv,'repeated_curve_cells':len(common)*16,'max_fit_rmse':max(v['rmse']for v in fits.values()),'OHLC':selected})
            except (ValueError,AssertionError,KeyError)as e:failures.append({'prefix':prefix,'error':str(e)})
    out={'baseline_21_cases':bases,'cases':cases,'failures':failures,'scope':'Finite START sweeps, fixed END and native1m source/chart; generator remains unknown.'}
    (ROOT/'C_START_regimenes.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'cases':[{k:v for k,v in c.items()if k!='OHLC'}for c in cases],'failures':failures},indent=2))
if __name__=='__main__':main()
