"""Selecciona dos ventanas nuevas por OHLC normalizado, sin leer sus curvas."""
import json, math, datetime, hashlib
from analizar_C_fuente_vs_grafico import ROOT, read

def shape(rows):
    lo=min(r['low'] for r in rows);hi=max(r['high'] for r in rows)
    return [(r[k]-lo)/(hi-lo) for r in rows for k in ['open','high','low','close']]

def main():
    data=json.loads((ROOT/'C_dataset_verificado.json').read_text())['cases']
    templates=[c for c in data if c['split']=='training' and c['dt']==60 and c['bars']==21
               and abs(c['C']-50)<1e-7]
    assert len(templates)==3
    source=read('C_VOL_1m_b.csv');candidates=[];utc=datetime.timezone.utc
    for t in sorted(source):
        date=datetime.datetime.fromtimestamp(t,utc)
        if date.date()!=datetime.date(2026,10,13) or not 7<=date.hour<18:continue
        stamps=list(range(t,t+21*60,60))
        if not all(s in source for s in stamps):continue
        r=[{'time':s,**{k:float(source[s][k]) for k in ['open','high','low','close']}} for s in stamps]
        R=max(x['high'] for x in r)-min(x['low'] for x in r)
        if R<5:continue
        vec=shape(r);dist=[(math.sqrt(sum((a-b)**2 for a,b in zip(vec,shape(c['OHLC'])))/84),c['id']) for c in templates]
        score,template=min(dist)
        candidates.append({'START':date.isoformat(),'END':datetime.datetime.fromtimestamp(stamps[-1],utc).isoformat(),
                           'distance_RMS':score,'nearest_template':template,'OHLC':r,'range':R})
    selected=[]
    for c in sorted(candidates,key=lambda x:(x['distance_RMS'],x['START'])):
        if any(not(c['OHLC'][-1]['time']<p['OHLC'][0]['time'] or c['OHLC'][0]['time']>p['OHLC'][-1]['time']) for p in selected):continue
        c['id']=f'replica24_{len(selected)+1}';c['prediction_C']=50
        c['extension_predictions']={'22_bars':52,'23_bars':55,'24_bars':57}
        selected.append(c)
        if len(selected)==2:break
    assert len(selected)==2
    out={'selection':'Two lowest RMS normalized full OHLC shapes to three observed21bar C50 templates. 13oct07..17 UTC, continuous1m, range>=5, selections nonoverlapping. No target C or plot consulted; no similarity cutoff fitted.',
         'scope':'Exploratory replication search, not a validated classifier or general C formula. Similarity may be incidental. Numerical prediction50 is frozen before target measurements; extend only if21bar50 passes.',
         'candidate_count':len(candidates),'template_ids':[c['id'] for c in templates], 'cases':selected}
    (ROOT/'C_replica24_predicciones.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({**out,'cases':[{k:v for k,v in c.items() if k!='OHLC'} for c in selected]},indent=2))

if __name__=='__main__':main()
