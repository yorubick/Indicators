"""Mediciones exploratorias sin optimizar longitudes ni umbrales según C."""
import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from analizar_C_frontera_1s import read
from analizar_C_bordes26 import stamp
from analizar_C_fuente_vs_grafico import fit_lite
from analizar_C_traslacion50 import comparison

ROOT=Path(__file__).parent
PERIODS=[24,89/3,8,89/9,72/27,89/27,72,89]

def sign(x):return 1 if x>0 else -1 if x<0 else 0

def ema_series(rows,N,offset):
    alpha=2/(N+1);previous=None;result={}
    for t,r in sorted(rows.items()):
        p=float(r['close'])
        previous=p+offset if previous is None else previous+alpha*(p-previous)
        result[t]=previous
    return result

def cloud_state(p,a,b):
    return 'above' if p>max(a,b) else 'below' if p<min(a,b) else 'inside'

def groups(results,key):
    d=defaultdict(list)
    for r in results:d[json.dumps(r[key],sort_keys=True)].append({'id':r['id'],'C':r['C']})
    return [{'signature':json.loads(k),'cases':v,'different_C':len({r['C'] for r in v})>1} for k,v in d.items() if len(v)>1]

def main():
    path=ROOT/'manual'/(sys.argv[1] if len(sys.argv)>1 else 'C_simetria1855_base.csv')
    output='C_geometria_ema_historia_larga' if len(sys.argv)>1 else 'C_geometria_ema'
    cases=json.loads((ROOT/'C_matriz_bordes_resultados.json').read_text())['all_cases']
    rows={t:r for t,r in read(path).items() if t<=stamp('19:21')}
    assert all(t in rows for t in range(min(rows),stamp('19:21')+1,60))
    emas={N:ema_series(rows,N,0) for N in PERIODS}
    plus={N:ema_series(rows,N,100) for N in PERIODS}
    minus={N:ema_series(rows,N,-100) for N in PERIODS}
    results=[]
    for case in cases:
        s,e=stamp(case['START']),stamp(case['END']);ts=list(range(s,e+1,60))
        R=case['H']-case['L'];lo=case['L']
        prices=[float(rows[t]['close']) for t in ts]
        variation=sum(abs(b-a) for a,b in zip(prices,prices[1:]))
        midpoint=(len(ts)-1)/2
        slope=sum((i-midpoint)*p for i,p in enumerate(prices))/sum((i-midpoint)**2 for i in range(len(ts)))
        def shape(t):
            r={k:float(rows[t][k]) for k in ['open','high','low','close']}
            return {'open_position':(r['open']-lo)/R,'close_position':(r['close']-lo)/R,
                    'absolute_body':abs(r['close']-r['open'])/R,
                    'upper_wick':(r['high']-max(r['open'],r['close']))/R,
                    'lower_wick':(min(r['open'],r['close'])-r['low'])/R}
        geometry={'START':shape(s),'END':shape(e),'efficiency':abs(prices[-1]-prices[0])/variation,
                  'normalized_variation':variation/R,'signed_slope_per_bar':slope/R,
                  'mean_absolute_body':sum(shape(t)['absolute_body'] for t in ts)/len(ts),
                  'mean_upper_wick':sum(shape(t)['upper_wick'] for t in ts)/len(ts),
                  'mean_lower_wick':sum(shape(t)['lower_wick'] for t in ts)/len(ts)}
        measures=[]
        for N in PERIODS:
            entry={'period_bars':N}
            for label,t in [('START',s),('END',e)]:
                p=float(rows[t]['close'])
                entry[label]={'distance':(p-emas[N][t])/R,'one_bar_slope':(emas[N][t]-emas[N][t-60])/R,
                              'sign':sign(p-emas[N][t]),'sign_stable_under_seed_100':sign(p-plus[N][t])==sign(p-minus[N][t]),
                              'seed100_distance_effect':abs(plus[N][t]-emas[N][t])/R,
                              'retained_seed_coefficient':(1-2/(N+1))**((t-min(rows))//60)}
            entry['crossings']=sum(sign(float(rows[t]['close'])-emas[N][t])!=sign(float(rows[t-60]['close'])-emas[N][t-60]) for t in ts[1:])
            measures.append(entry)
        signature={label:[m[label]['sign'] for m in measures[:6]] for label in ['START','END']}
        cloud_signature={label:[cloud_state(float(rows[t]['close']),emas[a][t],emas[b][t]) for a,b in zip(PERIODS[:6:2],PERIODS[1:6:2])] for label,t in [('START',s),('END',e)]}
        stability={label:[cloud_state(float(rows[t]['close']),plus[a][t],plus[b][t])==cloud_state(float(rows[t]['close']),minus[a][t],minus[b][t]) for a,b in zip(PERIODS[:6:2],PERIODS[1:6:2])] for label,t in [('START',s),('END',e)]}
        widths={label:[abs(emas[a][t]-emas[b][t])/R for a,b in zip(PERIODS[:6:2],PERIODS[1:6:2])] for label,t in [('START',s),('END',e)]}
        order={label:sorted(range(6),key=lambda i:emas[PERIODS[i]][t]) for label,t in [('START',s),('END',e)]}
        extended_signature={'signs':signature,'crossings':[m['crossings'] for m in measures[:6]],'endpoint_EMA_order':order}
        results.append({'id':case['START']+'_'+case['END'],'C':round(case['C']),'n':case['n'],
                        'H':case['H'],'L':case['L'],'prehistory_bars':(s-min(rows))//60,
                        'geometry':geometry,'EMA_measurements':measures,'endpoint_sign_signature':signature,
                        'cloud_signature':cloud_signature,'cloud_signature_seed100_stability':stability,
                        'cloud_absolute_widths':widths,'extended_signature':extended_signature})
    out={'measurement_spec':'C_GEOMETRIA_EMA_MEDICIONES.json','source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'periods':PERIODS,'results':results,'same_sign_groups':groups(results,'endpoint_sign_signature'),
         'same_cloud_groups':groups(results,'cloud_signature'),'same_extended_groups':groups(results,'extended_signature'),
         'limits':'Known labels, exploratory. Fixed EMA proxies not proven author lengths. +/-100 seed sensitivity is not guaranteed true-history bound. No predictor fitted.'}
    if len(sys.argv)>1:
        native=read(ROOT/'manual/C_simetria1855_base.csv')
        full=read(path)
        out['expanded_history_check']=comparison(native,full)
        out['expanded_history_Lite_fits']=fit_lite(full,60,60)
        assert all(abs(v['C']-62)<1e-6 for v in out['expanded_history_Lite_fits'].values())
    (ROOT/(output+'_resultados.json')).write_text(json.dumps(out,indent=2),encoding='utf-8')
    with (ROOT/(output+'_tabla.csv')).open('w',newline='',encoding='utf-8-sig') as f:
        cols=['id','C','n','start_close_position','end_close_position','efficiency','variation','mean_body','cloud_start','cloud_end']
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
        for r in results:
            g=r['geometry'];w.writerow(dict(zip(cols,[r['id'],r['C'],r['n'],g['START']['close_position'],g['END']['close_position'],g['efficiency'],g['normalized_variation'],g['mean_absolute_body'],str(r['cloud_signature']['START']),str(r['cloud_signature']['END'])])))
    print(json.dumps({'summary':[{'id':r['id'],'C':r['C'],'efficiency':round(r['geometry']['efficiency'],6),'start_pos':round(r['geometry']['START']['close_position'],6),'end_pos':round(r['geometry']['END']['close_position'],6),'cloud_signature':r['cloud_signature']} for r in results],
                      'same_sign_groups':out['same_sign_groups'],'same_cloud_groups':out['same_cloud_groups']},indent=2))

if __name__=='__main__':main()
