"""Audita frontera18..24 en dos ventanas elegidas antes de observar resultados."""
import datetime,json
from analizar_C_fuente_vs_grafico import ROOT,read,fit_lite,COLS
from obtener_C import recover
def main():
    cases=[];failures=[]
    for hour in [6,14]:
        for n in range(18,25):
            prefix=f'C_frontera_nueva_{hour:02d}00_{n}'
            pairs=('c','d') if (ROOT/'manual'/f'{prefix}_d.csv').exists() else ('a','b')
            path=ROOT/'manual'/f'{prefix}_{pairs[1]}.csv'
            if not path.exists():continue
            try:
                a,b=[read(f'{prefix}_{s}.csv') for s in pairs];common=set(a)&set(b)
                assert common and all(a[t][k]==b[t][k] for t in common for k in COLS),'pareja no estable'
                start=int(datetime.datetime(2026,10,12,hour,tzinfo=datetime.timezone.utc).timestamp());end=start+(n-1)*60
                timestamps=list(range(start,end+1,60));assert all(t in b for t in timestamps),'faltan OHLC rango'
                selected=[b[t] for t in timestamps];fits=fit_lite(b,60,60);Cs=[v['C'] for v in fits.values()];C=sum(Cs)/6
                assert max(Cs)-min(Cs)<1e-7 and max(v['rmse'] for v in fits.values())<1e-8,'Lite no sigue familia'
                ct=recover(path);interval=ct['C_seconds_interval']
                assert interval['lower_inclusive']-1e-8<=C<interval['upper_exclusive']+1e-8,f"Character incompatible {interval} vs Lite {C}"
                prediction=max(60,n*600/183)
                close=[float(r['close']) for r in selected];pathlength=sum(abs(y-x) for x,y in zip(close,close[1:]))
                cases.append({'prefix':prefix,'suffixes':pairs,'START':datetime.datetime.fromtimestamp(start,datetime.timezone.utc).isoformat(),'END':datetime.datetime.fromtimestamp(end,datetime.timezone.utc).isoformat(),'bars':n,'C':C,'short_rule_prediction':prediction,'short_rule_match':abs(C-prediction)<1e-7,'Character_interval':interval,'max_Lite_fit_rmse':max(v['rmse'] for v in fits.values()),'repeated_curve_cells':len(common)*16,'high':max(float(r['high']) for r in selected),'low':min(float(r['low']) for r in selected),'close_change':close[-1]-close[0],'close_path_length':pathlength,'OHLC':[{'time':t,**{k:float(b[t][k]) for k in ['open','high','low','close']}} for t in timestamps]})
            except (ValueError,AssertionError,KeyError) as e:failures.append({'prefix':prefix,'error':str(e)})
    shifts=[]
    for hour in [6,14]:
        prefix=f'C_frontera_shift_{hour:02d}01';path=ROOT/'manual'/f'{prefix}_d.csv'
        if not path.exists():continue
        try:
            a,b=[read(f'{prefix}_{s}.csv') for s in ['c','d']];common=set(a)&set(b)
            assert common and all(a[t][k]==b[t][k] for t in common for k in COLS),'pareja shift no estable'
            start=int(datetime.datetime(2026,10,12,hour,1,tzinfo=datetime.timezone.utc).timestamp());timestamps=list(range(start,start+21*60,60))
            assert all(t in b for t in timestamps),'faltanOHLC shift'
            fits=fit_lite(b,60,60);Cs=[v['C'] for v in fits.values()];C=sum(Cs)/6;ct=recover(path);interval=ct['C_seconds_interval']
            assert max(Cs)-min(Cs)<1e-7 and max(v['rmse'] for v in fits.values())<1e-8,'Lite shift no familia'
            assert interval['lower_inclusive']-1e-8<=C<interval['upper_exclusive']+1e-8,'Character shift incompatible'
            selected=[b[t] for t in timestamps];base=next(c for c in cases if c['START'][11:16]==f'{hour:02d}:00' and c['bars']==21)
            shifts.append({'prefix':prefix,'bars':21,'START':datetime.datetime.fromtimestamp(start,datetime.timezone.utc).isoformat(),'C':C,'baseline_C':base['C'],'high':max(float(r['high']) for r in selected),'low':min(float(r['low']) for r in selected),'baseline_high':base['high'],'baseline_low':base['low'],'Character_interval':interval,'repeated_curve_cells':len(common)*16,'removed_bar':base['OHLC'][0],'added_bar':{'time':timestamps[-1],**{k:float(selected[-1][k]) for k in ['open','high','low','close']}},'OHLC':[{'time':t,**{k:float(b[t][k]) for k in ['open','high','low','close']}} for t in timestamps]})
        except (ValueError,AssertionError,KeyError,StopIteration) as e:failures.append({'prefix':prefix,'error':str(e)})
    out={'configuration':{'date':'2026-10-12','chart_source_seconds':60,'Lite_source':'1m','Character_source':'Chart','starts_predeclared':['06:00','14:00']},'cases':cases,'shifts':shifts,'failures':failures,'scope':'Finite predeclared controls; no universal threshold or general C generator established.'}
    (ROOT/'C_fronteras_nuevas.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'cases':[{k:v for k,v in c.items() if k not in ['OHLC','repeated_curve_cells']} for c in cases],'shifts':[{k:v for k,v in c.items() if k!='OHLC'} for c in shifts],'failures':failures},indent=2))
if __name__=='__main__':main()
