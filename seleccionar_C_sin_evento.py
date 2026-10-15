"""Selección prospectiva por OHLC solamente, sin usar C de los rangos nuevos."""
import json,datetime
from analizar_C_fuente_vs_grafico import ROOT,read
from lab_base_C import states
def main():
    rows=read('C_VOL_1m_b.csv');known=json.loads((ROOT/'C_dataset_verificado.json').read_text())['cases'];occupied={(c['OHLC'][0]['time'],c['OHLC'][-1]['time'],c['dt'])for c in known};selected=[]
    z=datetime.timezone.utc
    for hour in range(6,19):
        for minute in range(60):
            start=int(datetime.datetime(2026,10,13,hour,minute,tzinfo=z).timestamp());ts=list(range(start,start+22*60,60))
            if not all(t in rows for t in ts):continue
            if selected and start<=selected[-1]['END_after_timestamp']:continue
            if (ts[0],ts[-2],60)in occupied or (ts[0],ts[-1],60)in occupied:continue
            bars=[{'time':t,**{k:float(rows[t][k])for k in ['open','high','low','close']}}for t in ts];hist=list(states(bars));a,b=hist[-2:];R=b['high']-b['low']
            events={'newH':b['new_high'],'newL':b['new_low'],'pivotH':a['last_confirmed_high']!=b['last_confirmed_high'],'pivotL':a['last_confirmed_low']!=b['last_confirmed_low']}
            if any(events.values())or R<5:continue
            selected.append({'id':f'noevent_{len(selected)+1}','START':datetime.datetime.fromtimestamp(start,z).isoformat(),'END_before':datetime.datetime.fromtimestamp(ts[-2],z).isoformat(),'END_after':datetime.datetime.fromtimestamp(ts[-1],z).isoformat(),'END_after_timestamp':ts[-1],'source_seconds':60,'bars_before':21,'bars_after':22,'range_points':R,'events':events,'prediction_delta_C':0,'OHLC':bars})
            if len(selected)==2:break
        if len(selected)==2:break
    assert len(selected)==2
    out={'selection':'13oct06..18, chronological first two nonoverlapping22bar windows with range>=5 and no defined record/radio1 event at last bar, not previously measured; OHLC only, C not consulted.','prediction_scope':'Restricted operational hypothesis: C changes only on one of these four events; predicts unchanged C at21->22. This can be refuted, but is not a complete generator.','cases':selected}
    (ROOT/'C_sin_evento_predicciones.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps([{k:v for k,v in c.items()if k!='OHLC'}for c in selected],indent=2))
if __name__=='__main__':main()
