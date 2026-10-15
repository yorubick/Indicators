"""Volumen nativo15s: unión exacta, escala común y suficiencia de pico."""
import json,sys,math,itertools
from analizar_C_fuente_vs_grafico import ROOT,read
from probar_C_volumen import metrics

SPEC={'sources':['C_recorte1903_30_c.csv','C_recorte1903_30_d.csv'],
 'join':'All selected timestamps must have identical OHLC and Volume in both closed-bar exports. Native15s, no disaggregation of1m.',
 'simple_models':'Same22 volume features from previous1m test, raw=n*dt*10/183*feature. Common K>0 across nine cases; observed C+/-1second generous necessary interval.',
 'peak_descriptor':'dt,n,H,L,ENDclose,peak_volume_timestamp,peak_volume_value,peak_barOHLC; first timestamp wins ties. Identical descriptor and differentC rejects any function exclusively of those inputs.',
 'suffix_descriptor':'dt,END and last80 complete OHLCV bars; not n or earlier history. Sufficiency only, no fitted classifier.',
 'scope':'Known overlapping local9, exploratory. No training32/reserved validation. Rejects explicit simple families only, not all volume dependence.'}

def main():
    p=ROOT/'C_volumen_frontera_preregistro.json'
    if '--spec' in sys.argv:
        p.write_text(json.dumps(SPEC,indent=2),encoding='utf-8');print('Reglas guardadas.');return
    assert json.loads(p.read_text())==SPEC
    a,b=[read(s) for s in SPEC['sources']]
    cases=json.loads((ROOT/'C_matriz_frontera15s.json').read_text())['cases'];joined=[]
    for c in cases:
        rows=[]
        for r in c['OHLC']:
            t=r['time'];assert t in a and t in b
            assert all(float(a[t][k])==float(b[t][k])==r[k] for k in ['open','high','low','close'])
            v=float(a[t]['Volume']);assert v==float(b[t]['Volume']) and v>=0
            rows.append({**r,'volume':v})
        assert all(y['time']-x['time']==15 for x,y in zip(rows,rows[1:]))
        joined.append({**c,'OHLC':rows})
    (ROOT/'C_matriz_frontera15s_volumen.json').write_text(json.dumps({'spec':SPEC,'cases':joined},indent=2),encoding='utf-8')
    f=[metrics(c) for c in joined];names=sorted(set.intersection(*(set(x) for x in f)));models=[]
    for name in names:
        raw=[c['bars']*c['dt']*10/183*x[name] for c,x in zip(joined,f)]
        if not all(math.isfinite(v) and v>0 for v in raw):continue
        low=max((round(c['C'])-1)/v for c,v in zip(joined,raw))
        high=min((round(c['C'])+1)/v for c,v in zip(joined,raw))
        models.append({'feature':name,'K_interval':[low,high],'survives':low<=high})
    peaks=[];suffix=[];details=[]
    for c in joined:
        rows=c['OHLC'];peak=max(rows,key=lambda r:r['volume']);H=max(r['high'] for r in rows);L=min(r['low'] for r in rows)
        key=(c['dt'],c['bars'],H,L,rows[-1]['close'],*(peak[k] for k in ['time','volume','open','high','low','close']))
        peaks.append(key);suffix.append((c['dt'],c['END'],tuple(tuple(r[k] for k in ['time','open','high','low','close','volume']) for r in rows[-80:])))
        details.append({'START':c['START'],'END':c['END'],'C':c['C'],'bars':c['bars'],
                        'first_volume':rows[0]['volume'],'total_volume':sum(r['volume'] for r in rows),
                        'peak_bar':peak,'volume_rank_first':1+sum(r['volume']>rows[0]['volume'] for r in rows)})
    def collisions(keys):
        return [{'case_A':details[i],'case_B':details[j]} for i,j in itertools.combinations(range(len(joined)),2) if keys[i]==keys[j] and abs(joined[i]['C']-joined[j]['C'])>1e-7]
    out={'spec':SPEC,'joined_cases':len(joined),'selected_bar_references_verified':sum(c['bars'] for c in joined),
         'models':models,'simple_models_surviving':sum(m['survives'] for m in models),
         'peak_descriptor_collisions':collisions(peaks),'last80_OHLCV_collisions':collisions(suffix),'details':details,
         'training32_used':False,'reserved_validation_used':False}
    (ROOT/'C_volumen_frontera_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'joined':len(joined),'features_tested':len(models),'survivors':out['simple_models_surviving'],
                      'peak_collisions':len(out['peak_descriptor_collisions']),'suffix_collisions':len(out['last80_OHLCV_collisions']),
                      'details':details,'first_peak_collision':out['peak_descriptor_collisions'][:1]},indent=2))

if __name__=='__main__':main()
