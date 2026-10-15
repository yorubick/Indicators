"""Verifica controles nativos15s y sus predicciones congeladas."""
import json
from analizar_C_fuente_vs_grafico import ROOT,read,fit_lite,COLS
from obtener_C import recover

def main():
    p=json.loads((ROOT/'C_rama24_resolucion_predicciones.json').read_text());cases=[];failures=[]
    for c in p['cases']:
        prefix=c['id'];pair=next(([a,b] for a,b in [('g','h'),('e','f'),('c','d')] if (ROOT/'manual'/f'{prefix}_{b}.csv').exists()),['c','d'])
        if not (ROOT/'manual'/f'{prefix}_{pair[1]}.csv').exists():continue
        try:
            a,b=[read(f'{prefix}_{s}.csv') for s in pair];common=set(a)&set(b)
            assert common and all(a[t][k]==b[t][k] for t in common for k in COLS),'unstable16curves'
            assert all(r['time'] in b and all(float(b[r['time']][k])==r[k] for k in ['open','high','low','close']) for r in c['OHLC']),'OHLCdiffers'
            fits=fit_lite(b,15,15);Cs=[v['C'] for v in fits.values()];C=sum(Cs)/6
            assert max(Cs)-min(Cs)<1e-7 and max(v['rmse'] for v in fits.values())<1e-8,'Litefamilyfailure'
            iv=recover(ROOT/'manual'/f'{prefix}_{pair[1]}.csv')['C_seconds_interval']
            assert iv['lower_inclusive']-1e-8<=C<iv['upper_exclusive']+1e-8,'Characterdisagrees'
            cases.append({k:v for k,v in c.items() if k!='OHLC'}|{'pair':pair,'C':C,'prediction_match':abs(C-c['prediction_C'])<1e-7,'repeat_cells':len(common)*16,'Character_interval':iv,'Lite_fits':fits})
        except (AssertionError,ValueError,KeyError,ZeroDivisionError) as e:failures.append({'id':prefix,'error':str(e)})
    out={'scope':'15s source=chart. END00 does not cover all of inclusive1m END; END45 does. No formula or branch classification inferred.', 'cases':cases,'failures':failures}
    (ROOT/'C_rama24_resolucion_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'cases':[{k:v for k,v in c.items() if k!='Lite_fits'} for c in cases],'failures':failures},indent=2))

if __name__=='__main__':main()
