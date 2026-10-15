"""Hipótesis dirigidas de primera excursión y retorno; no ajusta a plots."""
import csv,json,math
from pathlib import Path
from datetime import datetime
import numpy as np
from obtener_C import recover
ROOT=Path(__file__).parent
def stamp(s):return int(datetime.fromisoformat('2026-10-12T'+s+'+00:00').timestamp())
def main():
    old=json.loads((ROOT/'C_sensibilidad_15s.json').read_text())
    extra=json.loads((ROOT/'C_barrido_ampliado.json').read_text())['new_controls']
    cases=[];arrays=[]
    for case in old['cases']+old['END_controls']+extra:
        if any(c['start']==case['START_UTC'] and c['end']==case['END_UTC'] for c in cases):continue
        p=Path(case['extraction']['file']);rec=recover(p)
        rows={int(r['time']):r for r in csv.DictReader(p.open(encoding='utf-8-sig'))}
        ts=list(range(stamp(case['START_UTC']),stamp(case['END_UTC'])+1,15))
        assert all(t in rows for t in ts)
        v=np.array([[float(rows[t][k]) for k in ('open','high','low','close')] for t in ts]);o,h,l,c=v.T
        f={};height=h.max()-l.min()
        for name,x in [('close',c),('hl2',(h+l)/2),('hlc3',(h+l+c)/3),('ohlc4',(o+h+l+c)/4)]:
            diff=np.diff(x);nz=np.flatnonzero(diff)
            first_sign=np.sign(diff[nz[0]]) if len(nz) else 0
            opposite=np.flatnonzero(diff*first_sign<0)
            if len(opposite):
                j=int(opposite[0]+1);f[name+'_first_reversal']=j*15
                amplitude=abs(x[j-1]-x[0])
                if amplitude:f[name+'_excursion_height_ratio']=float(height/amplitude)
            for fraction in (.025,.05,.1,.25,.5):
                hit=np.flatnonzero(abs(x[1:]-x[0])>=height*fraction)
                if len(hit):f[name+'_first_displacement_'+str(fraction)]=(int(hit[0])+1)*15
            exit_=np.flatnonzero((x[1:]>h[0])|(x[1:]<l[0]))
            if len(exit_):f[name+'_first_exit_initial_candle']=(int(exit_[0])+1)*15
            for seedname,seed in [('open',o[0]),('close',c[0]),('hl2',(h[0]+l[0])/2)]:
                side=0
                for j in range(1,len(x)):
                    now=np.sign(x[j]-seed)
                    if not side and now:side=now
                    elif side and now!=side:
                        f[name+'_first_return_'+seedname]=j*15;break
        cases.append({'start':case['START_UTC'],'end':case['END_UTC'],'file':str(p),
            'C':rec['compatible_integer_C_seconds'][0],'interval':rec['C_seconds_interval'],'features':f})
        arrays.append(v)
    shared=set.intersection(*(set(c['features']) for c in cases));scores=[]
    excluded=sorted(set.union(*(set(c['features']) for c in cases))-shared)
    for feature in sorted(shared):
        # A single positive multiplier must satisfy every measured C interval.
        lower=max(c['interval']['lower_inclusive']/c['features'][feature] for c in cases)
        upper=min(c['interval']['upper_exclusive']/c['features'][feature] for c in cases)
        ratios=[c['C']/c['features'][feature] for c in cases];K=math.exp(float(np.mean(np.log(ratios))))
        scores.append({'feature':feature,'K_lower':lower,'K_upper':upper,'exact_common_K':lower<upper,
            'max_relative_error_descriptive_fit':max(abs(K*c['features'][feature]/c['C']-1) for c in cases)})
    pairs=[]
    for i,(a,va) in enumerate(zip(cases,arrays)):
        for b,vb in zip(cases[i+1:],arrays[i+1:]):
            if a['start']!=b['start'] or a['C']==b['C']:continue
            n=min(len(va),len(vb));assert np.array_equal(va[:n],vb[:n])
            pairs.append({'start':a['start'],'END_a':a['end'],'C_a':a['C'],'END_b':b['end'],'C_b':b['C'],
                'identical_prefix_bars':n,'identical_prefix_seconds_open_to_open':(n-1)*15,
                'identical_first_event_descriptors':[k for k in sorted(shared) if a['features'][k]==b['features'][k]]})
    scores.sort(key=lambda s:s['max_relative_error_descriptive_fit'])
    out={'cases':cases,'models_with_all_events_defined':len(scores),
        'exact_common_K_models':int(sum(s['exact_common_K'] for s in scores)),'models':scores,
        'excluded_descriptors_missing_in_some_ranges':excluded,
        'same_initial_prefix_different_C':pairs,
        'scope':'Finite first-event rules on overlapping 15s windows of one day. K fit only descriptive; no independent validation. C extracted from original plots. No generator identified.'}
    (ROOT/'C_primer_tramo.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'cases':len(cases),'models':len(scores),'exact':out['exact_common_K_models'],
        'prefix_counterexamples':len(pairs),'best_descriptive_model':scores[0] if scores else None,
        'prefix_example':max(pairs,key=lambda p:p['identical_prefix_bars']) if pairs else None},indent=2))
if __name__=='__main__':main()
