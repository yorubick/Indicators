"""Controles15s publicados anteriores a v4 pero ausentes del conjunto112."""
import json
from datetime import datetime
from analizar_C_fuente_vs_grafico import ROOT,read,fit_lite,COLS
from obtener_C import recover
from auditar_Gemini_v4 import extract_function,translate_pine_engine
from auditar_Gemini_v31 import metrics

def main():
    py=extract_function('Gemini_v4_evaluador_recibido.py','predict_C');pine=translate_pine_engine()
    supplied=json.loads((ROOT/'Gemini_v4_cases112_recibidos.json').read_text());keys={(c['dt'],c['OHLC'][0]['time'],c['OHLC'][-1]['time']) for c in supplied}
    start=int(datetime.fromisoformat('2026-10-12T18:55:00+00:00').timestamp());records=[]
    for endtime in ['19:21:00','19:21:15','19:21:30','19:21:45','19:22:00']:
        tag=endtime.replace(':','');prefix=f'Lite_185500_{tag}_15s';a,b=[read(f'{prefix}_{s}.csv') for s in ['a','b']]
        common=set(a)&set(b);assert common and all(a[t][k]==b[t][k] for t in common for k in COLS)
        end=int(datetime.fromisoformat('2026-10-12T'+endtime+'+00:00').timestamp())
        selected=[{'time':t,**{k:float(b[t][k]) for k in ['open','high','low','close']}} for t in range(start,end+1,15)]
        fits=fit_lite(b,15,15);cs=[r['C'] for r in fits.values()];C=sum(cs)/6
        assert max(cs)-min(cs)<1e-7 and max(r['rmse'] for r in fits.values())<1e-8
        iv=recover(ROOT/'manual'/f'{prefix}_b.csv')['C_seconds_interval'];assert iv['lower_inclusive']-1e-8<=C<iv['upper_exclusive']+1e-8
        c={'id':prefix,'START':'2026-10-12T18:55:00+00:00','END':'2026-10-12T'+endtime+'+00:00','dt':15,'bars':len(selected),'OHLC':selected,'C':C}
        val,branch=py(c);assert abs(pine(c)-val)<1e-7
        records.append({k:v for k,v in c.items() if k!='OHLC'}|{'python_prediction':val,'branch':branch,'already_in112':(15,start,end) in keys,'repeat16cells':len(common)*16})
    out={'scope':'Five earlier published native15s controls; no certified unseen/prospective claim. No fitting. Reaudited pairs16curves and Lite/CharacterC.','metrics':metrics(records),'cases':records}
    (ROOT/'Gemini_v4_barrido15_auditoria.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
