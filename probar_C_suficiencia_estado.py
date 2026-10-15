"""Prueba de entradas idénticas con C distinto, solo32controles largos entrenamiento."""
import json
from pathlib import Path
from lab_base_C import states
ROOT=Path(__file__).parent
def descriptors(case):
    rows=case['OHLC'];s=list(states(rows))[-1];n=s['n'];r=s['high']-s['low'];end=rows[-1];start=rows[0]
    d={'dt':case['dt'],'n':n,'range':r,'H':s['high'],'L':s['low'],'newH':s['new_high'],'newL':s['new_low'],'ageH':n-1-s['idx_high'],'ageL':n-1-s['idx_low'],'age_pivotH':None if s['last_confirmed_high']is None else n-1-s['last_confirmed_high'],'age_pivotL':None if s['last_confirmed_low']is None else n-1-s['last_confirmed_low'],'END_OHLC':tuple(end[k]for k in ['open','high','low','close']),'START_OHLC':tuple(start[k]for k in ['open','high','low','close']),'END_position':(end['close']-s['low'])/r if r else None}
    prev=rows[-2];left=rows[-3];d['confirmedH_END']=prev['high']>left['high']and prev['high']>=end['high'];d['confirmedL_END']=prev['low']<left['low']and prev['low']<=end['low']
    return d
SIGNATURES={
 'count_range_flags':['dt','n','range','newH','newL'],
 'count_global_flags':['dt','n','H','L','newH','newL'],
 'count_global_flags_confirmation':['dt','n','H','L','newH','newL','confirmedH_END','confirmedL_END'],
 'count_global_ages_flags':['dt','n','H','L','ageH','ageL','newH','newL'],
 'count_global_ages_pivot_ages':['dt','n','H','L','ageH','ageL','age_pivotH','age_pivotL','newH','newL'],
 'count_global_END':['dt','n','H','L','END_OHLC'],
 'count_global_START':['dt','n','H','L','START_OHLC'],
 'global_END_flags':['dt','H','L','END_OHLC','newH','newL'],
 'global_ages_END':['dt','H','L','ageH','ageL','END_OHLC'],
 'global_ages_pivots_END':['dt','H','L','ageH','ageL','age_pivotH','age_pivotL','END_OHLC'],
 'all_relative_observable':['dt','n','H','L','ageH','ageL','age_pivotH','age_pivotL','newH','newL','START_OHLC','END_OHLC'],
}
def main():
    cases=[c for c in json.loads((ROOT/'C_dataset_verificado.json').read_text())['cases']if c['split']=='training'and c['branch']=='long'];desc=[descriptors(c)for c in cases];results=[]
    for name,fields in SIGNATURES.items():
        grouped={}
        for c,d in zip(cases,desc):grouped.setdefault(tuple(d[k]for k in fields),[]).append(c)
        collisions=[]
        for key,group in grouped.items():
            for i,a in enumerate(group):
                for b in group[i+1:]:
                    if abs(a['C']-b['C'])>1e-7:collisions.append({'inputs':dict(zip(fields,key)),'case_A':{'id':a['id'],'C':a['C']},'case_B':{'id':b['id'],'C':b['C']}})
        results.append({'signature':name,'fields':fields,'groups':len(grouped),'repeated_input_groups':sum(len(g)>1 for g in grouped.values()),'contradictory_pairs':len(collisions),'counterexamples':collisions[:3],'interpretation':'Insufficient for deterministic C'if collisions else 'No contradiction found; not validated, potentially unique inputs'})
    out={'training_long_cases':len(cases),'validation_used':False,'scope':'Exact signatures, no statistical fitting or thresholds. Absolute START/END omitted intentionally: timestamp+count would often identify a window, preventing informative collisions; no claim of clock independence. Added candidate features are not proven original inputs.','results':results}
    (ROOT/'C_suficiencia_estado.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
