"""Contraejemplos de selectores explícitos, sin ajustar coeficientes ni C."""
import json,sys
from itertools import combinations
from pathlib import Path
from datetime import datetime,timezone
from obtener_C import recover
ROOT=Path(__file__).parent

def pivots(rows,source,radius):
    high=[float(r['high' if source=='wick' else 'close']) for r in rows]
    low=[float(r['low' if source=='wick' else 'close']) for r in rows]
    events=[]
    for i in range(radius,len(rows)-radius):
        # Equal values on the right qualify; strictly exceeds all left values.
        if high[i]>max(high[i-radius:i]) and high[i]>=max(high[i+1:i+radius+1]):
            events.append((i,'H',high[i]))
        if low[i]<min(low[i-radius:i]) and low[i]<=min(low[i+1:i+radius+1]):
            events.append((i,'L',low[i]))
    return sorted(events)

def signature(case,source,radius,selector,scope):
    rows=case['OHLC'];events=pivots(rows,source,radius)
    pick=0 if selector.startswith('first_') else -1
    if selector.endswith('high_and_low'):
        highs=[p for p in events if p[1]=='H'];lows=[p for p in events if p[1]=='L']
        selected=sorted([highs[pick],lows[pick]]) if highs and lows else None
    elif selector.endswith('opposite_pair'):
        pairs=[(a,b) for a,b in zip(events,events[1:]) if a[1]!=b[1] and a[0]<b[0]]
        selected=list(pairs[pick]) if pairs else None
    else:
        selected=[events[pick]] if events else None
    if selected is None:return None
    first=selected[0][0];last=selected[-1][0]
    event_info=[{'UTC':datetime.fromtimestamp(int(rows[i]['time']),timezone.utc).isoformat(),'side':side,'price':price} for i,side,price in selected]
    # Full selected OHLC, not just a duration/height. Only closed within-range
    # samples can confirm a pivot: future candles outside END are never used.
    tail=rows[first:(last+1 if scope=='structure_only' else len(rows))]
    data=[{'time':int(r['time']),**{k:float(r[k]) for k in ('open','high','low','close')}} for r in tail]
    result={'events':event_info,'selected_OHLC':data}
    if scope=='to_END_with_global_extrema':result.update(high=case['high'],low=case['low'])
    return result

def main():
    position=sys.argv[1] if len(sys.argv)>1 else 'last'
    assert position in ('first','last')
    cases=json.loads((ROOT/'C_matriz.json').read_text())['cases']
    # Restrict to long branch; no warmup/floor assumptions imposed.
    cases=[c for c in cases if c['bars']>=21]
    for c in cases:c['C_interval']=recover(Path(c['file']))['C_seconds_interval']
    results=[]
    for source in ('wick','close'):
        for radius in (1,2):
            for selector in (position+'_high_and_low',position+'_opposite_pair',position+'_confirmed_pivot'):
                for scope in ('structure_only','to_END','to_END_with_global_extrema'):
                    groups={};missing=[]
                    for c in cases:
                        sig=signature(c,source,radius,selector,scope)
                        if sig is None:missing.append({'START':c['START'],'END':c['END']});continue
                        groups.setdefault(json.dumps(sig,sort_keys=True),[]).append(c)
                    witnesses=[];scaled_witnesses=[]
                    for key,group in groups.items():
                        for a,b in combinations(group,2):
                            if abs(a['C']-b['C'])>1e-7:
                                witnesses.append({'first':{k:a[k] for k in ('START','END','bars','C')},
                                                  'second':{k:b[k] for k in ('START','END','bars','C')},'identical_selected_input':json.loads(key)})
                            # Most permissive among no round / nearest / floor /
                            # ceil to integer seconds: allow C+-1 before dividing
                            # by total bars. Disjoint intervals reject all four.
                            alo=(a['C']-1)/a['bars'];ahi=(a['C']+1)/a['bars']
                            blo=(b['C']-1)/b['bars'];bhi=(b['C']+1)/b['bars']
                            if max(alo,blo)>min(ahi,bhi)+1e-8:
                                scaled_witnesses.append({'first':{k:a[k] for k in ('START','END','bars','C')},
                                  'second':{k:b[k] for k in ('START','END','bars','C')},
                                  'first_F_conservative_interval':[alo,ahi],'second_F_conservative_interval':[blo,bhi]})
                    results.append({'source':source,'radius':radius,'selector':selector,'scope':scope,
                                    'defined_cases':len(cases)-len(missing),'missing':missing,
                                    'contradictory_pairs':len(witnesses),'rejected_as_sole_input':bool(witnesses),'witnesses':witnesses[:2],
                                    'rejected_with_linear_total_count_factor':bool(scaled_witnesses),'count_factor_witnesses':scaled_witnesses[:2]})
    out={'cases':len(cases),'tested_selector_signatures':len(results),'rejected_signatures':sum(r['rejected_as_sole_input'] for r in results),
         'rejected_with_linear_count_factor':sum(r['rejected_with_linear_total_count_factor'] for r in results),
         'results':results,'scope':'Direct input collisions; no K, no regression, no global floor. A collision refutes dependence solely on selected signature, not a selector used with total count or prefix state. No collision is not validation. One date/overlapping ranges.'}
    out['position']=position
    filename='C_selectores_iniciales.json' if position=='first' else 'C_selectores_pivotes.json'
    (ROOT/filename).write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
    print(json.dumps([{k:v for k,v in r.items() if k not in ('missing','witnesses','count_factor_witnesses')} for r in results],indent=2))
    target=next(r for r in results if r['source']=='wick' and r['radius']==1 and r['selector']==position+'_confirmed_pivot' and r['scope']=='to_END_with_global_extrema')
    print(json.dumps(target['witnesses'],indent=2))
if __name__=='__main__':main()
