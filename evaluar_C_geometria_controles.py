"""Mismas medidas fuera de matriz; sin entrenamiento o selección por etiqueta."""
import json
import hashlib
from collections import defaultdict
from pathlib import Path
from medir_C_geometria_ema import PERIODS,ema_series,sign
from analizar_C_frontera_1s import read

ROOT=Path(__file__).parent

def main():
    path=ROOT/'manual/C_startSweep1920_geometria_historia_larga.csv'
    rows=read(path);ordered=sorted(rows);indices={t:i for i,t in enumerate(ordered)}
    master=json.loads((ROOT/'master_all_C_cases.json').read_text())
    matrix=json.loads((ROOT/'C_matriz_bordes_resultados.json').read_text())['all_cases']
    from analizar_C_bordes26 import stamp
    excluded_grid={(stamp(c['START']),stamp(c['END'])) for c in matrix}
    series={N:ema_series(rows,N,0) for N in PERIODS}
    plus={N:ema_series(rows,N,100) for N in PERIODS}
    minus={N:ema_series(rows,N,-100) for N in PERIODS}
    results=[];excluded=[]
    for case in master['cases']:
        if case['dt']!=60 or case['C_Lite'] is None or case['bars']<21:continue
        s,e=case['START_unix'],case['END_unix']
        if (s,e) in excluded_grid:
            excluded.append({'id':case['id'],'reason':'matrix timestamp pair'});continue
        stamps=list(range(s,e+1,60))
        if not all(t in rows for t in stamps) or s-60 not in rows:
            excluded.append({'id':case['id'],'reason':'current history coverage'});continue
        assert len(stamps)==case['bars']
        for r in case['OHLCV']:
            t=r['time']
            for k in ['open','high','low','close']:
                assert float(rows[t][k])==float(r[k]),(case['id'],k)
            # Master uses lower-case volume.
            volume=r.get('volume',r.get('Volume'))
            assert volume is not None and float(rows[t]['Volume'])==float(volume),(case['id'],'volume')
        hi=max(float(rows[t]['high']) for t in stamps);lo=min(float(rows[t]['low']) for t in stamps);R=hi-lo
        p=[float(rows[t]['close']) for t in stamps];tv=sum(abs(b-a) for a,b in zip(p,p[1:]));mid=(len(p)-1)/2
        def shape(t):
            a={k:float(rows[t][k]) for k in ['open','high','low','close']}
            return {'open_position':(a['open']-lo)/R,'close_position':(a['close']-lo)/R,'absolute_body':abs(a['close']-a['open'])/R,
                    'upper_wick':(a['high']-max(a['open'],a['close']))/R,'lower_wick':(min(a['open'],a['close'])-a['low'])/R}
        g={'START':shape(s),'END':shape(e),'efficiency':abs(p[-1]-p[0])/tv,'normalized_variation':tv/R,
           'signed_slope_per_bar':sum((i-mid)*v for i,v in enumerate(p))/sum((i-mid)**2 for i in range(len(p)))/R,
           'mean_absolute_body':sum(shape(t)['absolute_body'] for t in stamps)/len(stamps),
           'mean_upper_wick':sum(shape(t)['upper_wick'] for t in stamps)/len(stamps),'mean_lower_wick':sum(shape(t)['lower_wick'] for t in stamps)/len(stamps)}
        measurements=[]
        for N in PERIODS:
            m={'period':N,'crossings':sum(sign(float(rows[t]['close'])-series[N][t])!=sign(float(rows[t-60]['close'])-series[N][t-60]) for t in stamps[1:])}
            for label,t in [('START',s),('END',e)]:
                m[label]={'distance':(float(rows[t]['close'])-series[N][t])/R,'slope':(series[N][t]-series[N][t-60])/R,
                          'sign':sign(float(rows[t]['close'])-series[N][t]),
                          'stable':sign(float(rows[t]['close'])-plus[N][t])==sign(float(rows[t]['close'])-minus[N][t]),
                          'seed100_effect':abs(plus[N][t]-series[N][t])/R}
            measurements.append(m)
        signatures={};signature_stability={}
        for count in [6,8]:
            signatures[str(count)]={'signs':{label:[m[label]['sign'] for m in measurements[:count]] for label in ['START','END']},
                                    'crossings':[m['crossings'] for m in measurements[:count]],
                                    'order':{label:sorted(range(count),key=lambda i:series[PERIODS[i]][t]) for label,t in [('START',s),('END',e)]}}
            alternative=[]
            for variant in [plus,minus]:
                alternative.append({'signs':{label:[sign(float(rows[t]['close'])-variant[N][t]) for N in PERIODS[:count]] for label,t in [('START',s),('END',e)]},
                                    'crossings':[sum(sign(float(rows[t]['close'])-variant[N][t])!=sign(float(rows[t-60]['close'])-variant[N][t-60]) for t in stamps[1:]) for N in PERIODS[:count]],
                                    'order':{label:sorted(range(count),key=lambda i:variant[PERIODS[i]][t]) for label,t in [('START',s),('END',e)]}})
            signature_stability[str(count)]=all(sig==signatures[str(count)] for sig in alternative)
        results.append({'id':case['id'],'START':case['START'],'END':case['END'],'s':s,'e':e,'n':len(stamps),'C':case['C_Lite'],
                        'H':hi,'L':lo,'geometry':g,'EMA':measurements,'signatures':signatures,'prehistory_bars':indices[s],
                        'provenance':case['provenance'],'signature_seed100_stability':signature_stability})
    grouped={}
    for count in [6,8]:
        groups=defaultdict(list)
        for r in results:
            if r['signature_seed100_stability'][str(count)]:
                groups[json.dumps(r['signatures'][str(count)],sort_keys=True)].append(r)
        grouped[str(count)]=[{'signature':json.loads(key),'cases':[{'id':r['id'],'C':r['C']} for r in values],
                            'different_C':max(r['C'] for r in values)-min(r['C'] for r in values)>1e-6} for key,values in groups.items() if len(values)>1]
    out={'protocol':'C_GEOMETRIA_EMA_CONTROLES_PROTOCOLO.json','source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'master_sha256':hashlib.sha256((ROOT/'master_all_C_cases.json').read_bytes()).hexdigest(),'results':results,'excluded':excluded,
         'groups':grouped,'limitations':'Historical overlapping labels; no blind validation, fitting, or prediction. State-only mappings evaluated for fixed proxy periods.'}
    (ROOT/'C_geometria_controles_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'accepted':len(results),'excluded':len(excluded),'stable6':sum(all(m[k]['stable'] for m in r['EMA'][:6] for k in ['START','END']) for r in results),
                      'stable8':sum(all(m[k]['stable'] for m in r['EMA'] for k in ['START','END']) for r in results),
                      'collision_groups':{k:[g['cases'] for g in values if g['different_C']] for k,values in grouped.items()}},indent=2))

if __name__=='__main__':main()
