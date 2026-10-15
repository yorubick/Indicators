"""Comparación exploratoria declarada, sin ajuste a las etiquetas de C."""
import json,hashlib
from pathlib import Path
from collections import defaultdict
from analizar_C_frontera_1s import read
from analizar_C_bordes26 import stamp
from medir_C_geometria_ema import ema_series,sign,cloud_state

ROOT=Path(__file__).parent

def collisions(results,key):
    buckets=defaultdict(list)
    for r in results:buckets[json.dumps(r[key],sort_keys=True)].append({'END':r['END'],'C':r['C']})
    return [{'signature':json.loads(k),'cases':v} for k,v in buckets.items() if len({r['C'] for r in v})>1]

def main():
    spec=json.loads((ROOT/'C_END15_COMPARACION_ESPECIFICACION.json').read_text())
    path=ROOT/spec['source'];s=stamp('18:52');last=stamp('19:18')+45
    rows={t:r for t,r in read(path).items() if t<=last};times=sorted(rows)
    assert all(t in rows for t in range(times[0],last+1,15))
    baseline=json.loads((ROOT/'C_END15_barrido_resultados.json').read_text())['results']
    out={'specification':spec,'history_first_timestamp':times[0],'prehistory_bars':(s-times[0])//15,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'families':{}}
    for label,mult in [('fixed_bars',1),('same_seconds_as_1m_proxies',4)]:
        periods=[x*mult for x in spec['reference_EMA_periods_bars']]
        emas={p:ema_series(rows,p,0) for p in periods}
        variants={o:{p:ema_series(rows,p,o) for p in periods} for o in [-100,100]}
        results=[]
        for case in baseline:
            end=case['END'];e=stamp(end[:5])+int(end[-2:]);ts=list(range(s,e+1,15));price=float(rows[e]['close']);R=case['H']-case['L'];lo=case['L']
            measured=read(ROOT/'manual'/f'C_estructura15_barrido_{end.replace(":", "")}_b.csv')
            assert all(rows[t][k]==measured[t][k] for t in ts for k in ['open','high','low','close','Volume'])
            def discrete(series):
                signs=[sign(price-series[p][e]) for p in periods]
                slopes=[sign(series[p][e]-series[p][e-15]) for p in periods]
                crossings=[sum(sign(float(rows[t]['close'])-series[p][t])!=sign(float(rows[t-15]['close'])-series[p][t-15]) for t in ts[1:]) for p in periods]
                clouds=[cloud_state(price,series[a][e],series[b][e]) for a,b in zip(periods[:6:2],periods[1:6:2])]
                pairs=[sign(series[a][e]-series[b][e]) for a,b in zip(periods[:6:2],periods[1:6:2])]
                order=sorted(range(8),key=lambda i:series[periods[i]][e])
                return {'signs':signs,'slopes':slopes,'crossings':crossings,'clouds':clouds,'pair_order':pairs,'order':order}
            d=discrete(emas);stability=[discrete(variants[o])==d for o in [-100,100]]
            prices=[float(rows[t]['close']) for t in ts];variation=sum(abs(b-a) for a,b in zip(prices,prices[1:]))
            raw={k:float(rows[e][k]) for k in ['open','high','low','close','Volume']}
            r={'END':end,'C':round(case['C']),'n':len(ts),'signature':d,'seed100_signature_stability':stability,
               'signs':d['signs'],'clouds':d['clouds'],'sign_slope_cloud_order':{k:d[k] for k in ['signs','slopes','clouds','pair_order','order']},
               'EMA_distances':[(price-emas[p][e])/R for p in periods],
               'EMA_slopes':[(emas[p][e]-emas[p][e-15])/R for p in periods],
               'cloud_widths':[abs(emas[a][e]-emas[b][e])/R for a,b in zip(periods[:6:2],periods[1:6:2])],
               'body_sign':sign(raw['close']-raw['open']),'close_change_sign':sign(price-float(rows[e-15]['close'])),
               'mod3':len(ts)%3,'mod9':len(ts)%9,'mod27':len(ts)%27,
               'geometry':{'close_position':(price-lo)/R,'body':(raw['close']-raw['open'])/R,
                           'upper_wick':(raw['high']-max(raw['open'],raw['close']))/R,'lower_wick':(min(raw['open'],raw['close'])-raw['low'])/R,
                           'normalized_variation':variation/R,'efficiency':abs(price-prices[0])/variation,
                           'close_rank':sum(p<=price for p in prices)/len(prices),
                           'volume_rank':sum(float(rows[t]['Volume'])<=raw['Volume'] for t in ts)/len(ts)}}
            results.append(r)
        keys=['signature','signs','clouds','sign_slope_cloud_order','body_sign','close_change_sign','mod3','mod9','mod27']
        out['families'][label]={'periods_bars':periods,'results':results,'collisions':{k:collisions(results,k) for k in keys}}
    (ROOT/'C_END15_comparacion_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'prehistory_bars':out['prehistory_bars'],'families':{k:{'all_seed100_stable':all(all(r['seed100_signature_stability']) for r in v['results']),
          'collision_groups':{key:len(val) for key,val in v['collisions'].items()},'full_signature_collisions':v['collisions']['signature'],
          'table':[{key:r[key] for key in ['END','C','body_sign','close_change_sign','signs','clouds']} for r in v['results']]} for k,v in out['families'].items()}},indent=2))

if __name__=='__main__':main()
