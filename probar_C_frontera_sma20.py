"""C21 como período efectivo ajustado a la primera variación SMA20.

Se requiere n21 por una razón explícita: dos muestras SMA20 consecutivas.
No equivale al test previo de EMA con semilla SMA y objetivo END.
"""
import json,sys,itertools,math
from analizar_C_fuente_vs_grafico import ROOT

SOURCES=['close','hl2','hlc3','ohlc4']
SPEC={'cases':'Only master dataset training cases with exactly21 bars; reserved validation not used.',
 'target_series':SOURCES,'driver_series':SOURCES,
 'coefficient':'y0=mean(target bars0..19), y1=mean(target bars1..20); alpha=(y1-y0)/(driver_bar20-y0). Equivalent least-squares one-update fit y1=y0+alpha*(driver20-y0).',
 'policies':['positive','absolute'],
 'admissibility':'Denominator nonzero; coefficient (raw or absolute per fixed policy) must satisfy0<alpha<=1. No clipping or per-case fallback in long branch.',
 'mapping':'N=2/alpha-1; C=K*dt*N, one positiveK shared by all eleven trainingC21, generous observedC+/-1second intervals.',
 'short_branch':'Previously observed short relationship retained only as reference; matching its cutoff does not establish original mechanism.',
 'gate':'Reject incomplete coverage or empty commonK interval. Only survivors may be tested on other training lengths before reserved validation.',
 'scope':'32 finite candidates, known overlapping training labels. Exploratory. Does not exclude all rolling20 calculations, external series, initialization or postEND data.'}

def values(rows,source):
    if source=='close':return [r['close'] for r in rows]
    if source=='hl2':return [(r['high']+r['low'])/2 for r in rows]
    if source=='hlc3':return [(r['high']+r['low']+r['close'])/3 for r in rows]
    return [sum(r[k] for k in ['open','high','low','close'])/4 for r in rows]

def main():
    p=ROOT/'C_frontera_sma20_preregistro.json'
    if '--spec' in sys.argv:p.write_text(json.dumps(SPEC,indent=2),encoding='utf-8');print('32 reglas congeladas; solo entrenamiento21.');return
    assert json.loads(p.read_text())==SPEC
    dataset=json.loads((ROOT/'C_dataset_verificado.json').read_text());cases=[c for c in dataset['cases'] if c['bars']==21 and c['split']=='training']
    assert len(cases)==11
    transitions=[]
    for c in cases:
        pair=next((x for x in dataset['cases'] if x['split']=='training' and x['bars']==20 and x['dt']==c['dt'] and x['START']==c['START'] and x['OHLC']==c['OHLC'][:-1]),None)
        transitions.append({'id':c['id'],'dt':c['dt'],'C21':c['C'],'C20_measured':pair['C'] if pair else None,
                            'C21_short_continuation':21*c['dt']*10/183,'paired20_id':pair['id'] if pair else None})
    models=[]
    for target,driver,policy in itertools.product(SOURCES,SOURCES,SPEC['policies']):
        records=[];lo=0.;hi=math.inf
        for c in cases:
            ys=values(c['OHLC'],target);xs=values(c['OHLC'],driver)
            # Centered arithmetic avoids subtracting large nearly equal means.
            y0=ys[0]+sum(v-ys[0] for v in ys[:20])/20
            dy=(ys[20]-ys[0])/20;den=xs[20]-y0
            raw=dy/den if abs(den)>1e-12 else None
            a=abs(raw) if raw is not None and policy=='absolute' else raw
            admissible=a is not None and 0<a<=1
            rec={'id':c['id'],'C':c['C'],'alpha_raw':raw,'alpha_used':a,'admissible':admissible}
            if admissible:
                period=(2/a-1)*c['dt'];l=(round(c['C'])-1)/period;h=(round(c['C'])+1)/period
                lo=max(lo,l);hi=min(hi,h);rec.update(period_seconds=period,K_interval=[l,h])
                assert abs((y0+raw*den)-(y0+dy))<1e-8
            records.append(rec)
        full=all(r['admissible'] for r in records)
        models.append({'target':target,'driver':driver,'policy':policy,'admissible_cases':sum(r['admissible'] for r in records),
                       'K_interval_on_admissible':[lo,hi] if any(r['admissible'] for r in records) else None,
                       'survives_all11':full and lo<=hi,'cases':records})
    out={'spec':SPEC,'training21_count':len(cases),'paired20_count':sum(t['paired20_id'] is not None for t in transitions),
         'transitions':transitions,'model_count':len(models),'survivors':sum(m['survives_all11'] for m in models),
         'models':models,'reserved_validation_used':False,'master_dataset_modified':False}
    (ROOT/'C_frontera_sma20_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ['spec','models']},indent=2))
    print(json.dumps([{'target':m['target'],'driver':m['driver'],'policy':m['policy'],'coverage':m['admissible_cases'],'K':m['K_interval_on_admissible']} for m in models if m['admissible_cases']==11],indent=2))

if __name__=='__main__':main()
