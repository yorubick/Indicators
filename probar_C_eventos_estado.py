"""Condiciones necesarias/suficientes de eventos, no ajuste de valores de C."""
import json
from pathlib import Path
from lab_base_C import states
ROOT=Path(__file__).parent
def main():
    cases=[c for c in json.loads((ROOT/'C_dataset_verificado.json').read_text())['cases']if c['split']=='training'and c['branch']=='long'];families={}
    for c in cases:families.setdefault((c['dt'],c['START']),[]).append(c)
    transitions=[]
    for (dt,start),group in families.items():
        group.sort(key=lambda c:c['END'])
        for a,b in zip(group,group[1:]):
            if b['OHLC'][-1]['time']-a['OHLC'][-1]['time']!=dt:continue
            assert a['OHLC']==b['OHLC'][:-1]
            history=list(states(b['OHLC']));prev,end=history[-2:];events={'new_global_H':end['new_high'],'new_global_L':end['new_low'],'new_confirmed_local_H':end['last_confirmed_high']!=prev['last_confirmed_high'],'new_confirmed_local_L':end['last_confirmed_low']!=prev['last_confirmed_low']};changed=abs(b['C']-a['C'])>1e-7
            transitions.append({'START':start,'END_before':a['END'],'END_after':b['END'],'C_before':a['C'],'C_after':b['C'],'C_changed':changed,'delta_C':b['C']-a['C'],'events':events,'any_event':any(events.values()),'same_global_extrema':prev['high']==end['high']and prev['low']==end['low'],'added_bar':b['OHLC'][-1]})
    absent_changes=[t for t in transitions if t['C_changed']and not t['any_event']];present_nochanges=[t for t in transitions if not t['C_changed']and t['any_event']]
    out={'transitions':transitions,'counts':{'closed_consecutive_END_transitions':len(transitions),'C_change_without_defined_event':len(absent_changes),'defined_event_without_C_change':len(present_nochanges)},'no_event_change_witnesses':absent_changes[:4],'event_no_change_witnesses':present_nochanges[:4],'scope':'Training only, adjacent END additions, strict first-record H/L and radio1 pivot detector. Tests only these events; other events, count, leg ages, state initialization remain possible. No causal price edit, no formula of C.'}
    (ROOT/'C_eventos_estado.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in out.items()if k!='transitions'},indent=2))
if __name__=='__main__':main()
