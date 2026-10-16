"""Congela y emula la regla pegada por el usuario; evaluación solo de entrenamiento."""
import json,math,hashlib
from pathlib import Path
ROOT=Path(__file__).parent
ATTACHMENT=Path(r'C:\Users\PC\.codex\attachments\cb050007-d0d6-4b90-9073-4c690a9fb42d\Texto pegado.txt')
def candidate(case):
    rows=case['OHLC'];n=len(rows);dt=case['dt'];high=rows[0]['high'];low=rows[0]['low'];previous_high=high
    for row in rows[1:]:
        previous_high=high;high=max(high,row['high']);low=min(low,row['low'])
    new_high=rows[-1]['high']>previous_high;span=(n-1)*dt;R=high-low
    if n<21:C=max(dt,n*dt*10/183);branch='short'
    elif R<=22.25 and not new_high and n<=25:C=math.floor(span/24);branch='A_consolidation'
    elif new_high and R<=26:C=71;branch='B_new_high'
    else:C=77;branch='C_default_macro'
    return {'C':C,'branch':branch,'range_points':R,'new_high_at_END':new_high,'previous_global_high':previous_high,'END_high':rows[-1]['high'],'time_span_seconds':span,'bars':n}
def main():
    attached=ATTACHMENT.read_text(encoding='utf-8-sig');pine=attached[attached.index('//@version=5'):].strip()+'\n';digest=hashlib.sha256(pine.encode()).hexdigest();(ROOT/'pine/Gemini_estados_v2_recibido.pine').write_text(pine,encoding='utf-8')
    assert all(s in pine for s in ['rng_pts <= 22.25','bar_cnt <= 25','rng_pts <= 26.0','C_calc := 71.0','C_calc := 77.0'])
    dataset=json.loads((ROOT/'C_dataset_verificado.json').read_text());train=[c for c in dataset['cases']if c['split']=='training'];results=[]
    for c in train:
        prediction=candidate(c);error=prediction['C']-c['C'];results.append({'id':c['id'],'START':c['START'],'END':c['END'],'dt':c['dt'],'bars':c['bars'],'original_C':c['C'],'prediction':prediction,'error_seconds':error,'match':abs(error)<1e-7})
    summary={b:{'cases':sum(r['bars']<21 if b=='short'else r['bars']>=21 for r in results),'matches':sum(r['match']and(r['bars']<21 if b=='short'else r['bars']>=21)for r in results)}for b in ['short','long']}
    counts={name:{'cases':sum(r['prediction']['branch']==name for r in results),'matches':sum(r['match']and r['prediction']['branch']==name for r in results)}for name in ['short','A_consolidation','B_new_high','C_default_macro']}
    out={'source_attachment':str(ATTACHMENT),'frozen_pine_sha256':digest,'summary':summary,'branches':counts,'validation_status':'Not evaluated: candidate must pass all training before validation. No fitting or threshold optimization performed.','scope':'Offline emulation of supplied final-bar rules on aligned native-source charts. Pine not compiled or installed. Code updates range every bar but classifies only at END; no swing/leg state or stored breakout C.','cases':results}
    (ROOT/'Gemini_estados_v2_auditoria.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items()if k!='cases'},indent=2));print(json.dumps([r for r in results if r['bars']>=21 and not r['match']][:8],indent=2))
if __name__=='__main__':main()
