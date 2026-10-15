"""Control cruzado de END, historial cerrado y semilla, independiente del ajuste local EMA.

No certifica START por sí solo ni obtiene el generador de C.
"""
import csv,json
from pathlib import Path
from probar_C_estructura import load,stamp
from obtener_C import recover
from flujo_manual import FlujoManual
ROOT=Path(__file__).parent

def main():
    old=json.loads((ROOT/'C_estructura.json').read_text())
    cases=old['training_cases']+old['reserved_cases']
    for c in json.loads((ROOT/'C_barrido_ampliado.json').read_text())['new_controls']:
        cases.append({'file':c['extraction']['file'],'start':c['START_UTC'],'end':c['END_UTC'],
                      'dt':15,'C':c['extraction']['compatible_integer_C_seconds'][0]})
    results=[]
    for case in cases:
        v,interval,fallback=load(case);extraction=recover(Path(case['file']));periods=extraction['periods']
        allrows=list(csv.DictReader(Path(case['file']).open(encoding='utf-8-sig')))
        available={int(r['time']):r for r in allrows[:-1]}
        start,end=stamp(case['start']),stamp(case['end']);dt=case['dt']
        borrowed=[]
        if fallback:
            supporting=list(csv.DictReader(Path(fallback).open(encoding='utf-8-sig')))[:-1]
            for r in supporting:
                t=int(r['time'])
                if t in available:
                    assert all(r[k]==available[t][k] for k in ('open','high','low','close')),case['file']
                elif end<t<=end+5400:
                    copy=dict(r)
                    for k in periods:copy[k]=''
                    available[t]=copy;borrowed.append(t)
        # Compare up to 90 minutes after END, with a regular complete source grid.
        limit=min(end+5400,max(available))
        needed=list(range(end+dt,limit+1,dt))
        missing=[t for t in needed if t not in available]
        if missing:
            limit=missing[0]-dt;needed=[t for t in needed if t<=limit]
        high=v[:,1].max();low=v[:,2].min()
        breakout=next((t for t in needed if float(available[t]['close'])>high or float(available[t]['close'])<low),None)
        firsts={k:next((t for t in needed if available[t][k]),None) for k in periods}
        sides=[]
        for side,index in [('low',2),('high',1)]:
            seed=float(v[-1,index]);state=dict.fromkeys(periods,seed);errors=[]
            for t in needed:
                r=available[t]
                for k,n in periods.items():
                    state[k]+=2/(n+1)*(float(r['close'])-state[k])
                    if r[k]:errors.append(abs(state[k]-float(r[k])))
            sides.append({'side':side,'seed':seed,'values':len(errors),
                          'max_error':max(errors) if errors else None})
        eligible=[s for s in sides if s['max_error'] is not None]
        best=min(eligible,key=lambda s:s['max_error']) if eligible else None
        causal=FlujoManual(case['C'],dt,float(high),float(low),float(v[-1,1]),float(v[-1,2]))
        assert causal.periods==periods,case['file']
        causal_errors=[];unexpected=0
        for t in needed:
            r=available[t];prediction=causal.closed_bar_after_END(float(r['close']))
            for k in periods:
                if r[k]:
                    if prediction is None:unexpected+=1
                    else:causal_errors.append(abs(prediction[k]-float(r[k])))
        breakout_side=('bull' if float(available[breakout]['close'])>high else 'bear') if breakout else None
        choices={'END_body':'low' if v[-1,3]>=v[-1,0] else 'high',
                 'range_net_close':'low' if v[-1,3]>=v[0,3] else 'high',
                 'first_breakout':'low' if breakout_side=='bull' else 'high' if breakout_side=='bear' else None}
        results.append({'file':case['file'],'start':case['start'],'end':case['end'],'dt':dt,'C':case['C'],
            'C_interval':interval,'OHLC_fallback':fallback,'post_END_OHLC_borrowed_count':len(borrowed),'checked_until_UTC_timestamp':limit,
            'truncated_at_missing_timestamp':missing[0] if missing else None,
            'first_strict_close_breakout':breakout,'first_plots':firsts,
            'visibility_matches':not borrowed and breakout is not None and all(t==breakout for t in firsts.values()),
            'visibility_status':'not_testable_missing_original_prefix' if borrowed else 'tested',
            'seed_candidates':sides,'best_seed':best,
            'seed_side_predictions':choices,'first_breakout_direction':breakout_side,
            'causal_reconstruction':{'values':len(causal_errors),'max_error':max(causal_errors) if causal_errors else None,
                'plots_before_prediction':unexpected,'chosen_direction':causal.side,
                'matches':len(causal_errors)>=50 and unexpected==0 and max(causal_errors)<1e-8},
            'reconstruction_matches':best is not None and best['values']>=50 and best['max_error']<1e-8})
    good=[r for r in results if r['reconstruction_matches']]
    prediction_scores={k:{'matches':sum(r['seed_side_predictions'][k]==r['best_seed']['side'] for r in good),
        'cases':len(good),'counterexamples':[{'start':r['start'],'end':r['end'],'dt':r['dt'],'C':r['C'],
         'actual_side':r['best_seed']['side'],'predicted_side':r['seed_side_predictions'][k]} for r in good if r['seed_side_predictions'][k]!=r['best_seed']['side']]} for k in ('END_body','range_net_close','first_breakout')}
    out={'case_count':len(results),'reconstructions_matching':sum(r['reconstruction_matches'] for r in results),
         'seed_direction_rules':prediction_scores,
         'causal_reconstructions_matching':sum(r['causal_reconstruction']['matches'] for r in results),
         'visibility_matching':sum(r['visibility_matches'] for r in results),
         'values_in_matching_reconstructions':sum(r['best_seed']['values'] for r in results if r['reconstruction_matches']),
         'scope':'Native Manual source=chart. Reconstructs AFTER END from END low/high and all later closes; checks all ten curves. END and recurrence control does not uniquely certify START. Earlier unpaired measurements still need UI repetition for definitive provenance.',
         'cases':results}
    (ROOT/'C_auditoria_ancla.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
    print(json.dumps([r for r in results if not r['reconstruction_matches'] or not r['visibility_matches']],indent=2))

if __name__=='__main__':main()
