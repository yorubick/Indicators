"""Preregistra duración/24 y comprueba cobertura nativa antes de medir C."""
import json,datetime,math
from analizar_C_fuente_vs_grafico import ROOT,read

def main():
    source=read('Lite_185500_192200_15s_b.csv')
    ds=json.loads((ROOT/'C_dataset_verificado.json').read_text())['cases'];out=[]
    for start,end in [('19:02','19:22'),('19:03','19:23')]:
        base=next(c for c in ds if c['START']==f'2026-10-12T{start}:00+00:00' and c['END']==f'2026-10-12T{end}:00+00:00' and c['dt']==60)
        for second in ['00','45']:
            T0=int(datetime.datetime.fromisoformat(base['START']).timestamp());T1=int(datetime.datetime.fromisoformat(f'2026-10-12T{end}:{second}+00:00').timestamp())
            rows=[{'time':t,**{k:float(source[t][k]) for k in ['open','high','low','close']}} for t in range(T0,T1+1,15)]
            aggregation=[]
            for m in base['OHLC']:
                rs=[source[m['time']+i] for i in [0,15,30,45]]
                a={'open':float(rs[0]['open']),'high':max(float(x['high']) for x in rs),'low':min(float(x['low']) for x in rs),'close':float(rs[-1]['close'])}
                aggregation.append(all(a[k]==m[k] for k in a))
            assert all(aggregation),'nativeOHLCnotidenticalto1m'
            out.append({'id':f'C_rama24_res_{start.replace(":","")}_{second}', 'START':base['START'],'END':f'2026-10-12T{end}:{second}+00:00','dt':15,'bars':len(rows),'prediction_C':math.floor((T1-T0)/24),'baseline_1m_C':base['C'],'coverage_matches_full_1m_window':second=='45','aggregation_exact':True,'OHLC':rows})
    p={'scope':'Fixed elapsed-time/24 candidate predicts50 at END00 and51 at END45. If C changes branch by resolution this formula need not apply; no generator identified. END45 covers the same physical price interval as inclusive1m END; END00 excludes last45seconds.', 'cases':out}
    (ROOT/'C_rama24_resolucion_predicciones.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in c.items() if k!='OHLC'} for c in out],indent=2))

if __name__=='__main__':main()
