"""Extrapolaciones locales registradas con OHLC conocido y C futuro no consultado."""
import json,datetime
from analizar_C_fuente_vs_grafico import ROOT,read
from lab_base_C import states
def ages(s):
    n=s['n'];return {'globalH':n-1-s['idx_high'],'globalL':n-1-s['idx_low'],'pivotH':n-1-s['last_confirmed_high'],'pivotL':n-1-s['last_confirmed_low']}
def main():
    rows=read('C_VOL_1m_b.csv');start=int(datetime.datetime(2026,10,13,6,25,tzinfo=datetime.timezone.utc).timestamp());ts=list(range(start,start+26*60,60));assert all(t in rows for t in ts)
    bars=[{'time':t,**{k:float(rows[t][k])for k in ['open','high','low','close']}}for t in ts];history=list(states(bars));base=ages(history[20]);after=ages(history[21]);assert all(after[k]==base[k]+1 for k in base)
    intercepts={k:87+3*a for k,a in base.items()};results=[]
    for i in range(20,26):
        s=history[i];a=ages(s);bar=bars[i];trend=bars[i-1]['close']-bars[0]['close'];body=bar['close']-bar['open'];prev=history[i-1];events={'newH':s['new_high'],'newL':s['new_low'],'pivotH':s['last_confirmed_high']!=prev['last_confirmed_high'],'pivotL':s['last_confirmed_low']!=prev['last_confirmed_low']}
        results.append({'END':datetime.datetime.fromtimestamp(ts[i],datetime.timezone.utc).isoformat(),'bars':i+1,'ages':a,'age_model_predictions':{k:intercepts[k]-3*a[k]for k in base},'linear_count_prediction':87-3*(i-20),'pullback_definition':{'prior_net_close_change':trend,'END_body':body,'countertrend_body':trend*body<0,'Gemini_predicted_delta_interval':[20,57]if trend*body<0 else None},'events':events,'range_high':s['high'],'range_low':s['low'],'END_OHLC':bar})
    out={'START':'2026-10-13T06:25:00+00:00','known_C_END45':87,'known_C_END46':84,'calibration':'Two known observations only: slope-3/age-step. Intercepts87+3*baseline_age; frozen before measuring END47..50. Fits are exploratory local predictions, not a general formula. Four age models initially indistinguishable; event changes can separate them. No floor or adjustment added.','age_model_intercepts':intercepts,'predictions':results,'OHLC':bars}
    (ROOT/'C_evolucion87_predicciones.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in out.items()if k!='OHLC'},indent=2))
if __name__=='__main__':main()
