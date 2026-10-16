"""Emulación independiente del generador híbrido Pine actual, sin ejecutarlo ni compilarlo."""
import math,json,hashlib,csv,datetime
from pathlib import Path
ROOT=Path(__file__).parent
SOURCE=Path(r'C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\PoiSzn_C_Detector_Lab.pine')
BASE={'Lane 3 A':24,'Lane 3 B':89/3,'Lane 2 A':8,'Lane 2 B':89/9,'Lane 1 A':72/27,'Lane 1 B':89/27,'Layer A':24,'Layer A boundary':89/3,'Layer B':8,'Layer B boundary':89/9,'Layer C':72/27,'Layer C boundary':89/27,'Extra cloud 1':72,'Extra cloud 1 boundary':89,'Extra cloud 2':216,'Extra cloud 2 boundary':267}
def pine_round(x):return math.floor(x+.5)
def predict(rows,dt=60,tick=.25):
    rows=[{k:float(r[k]) for k in ['open','high','low','close']} for r in rows]
    n=len(rows);high=max(r['high'] for r in rows);low=min(r['low'] for r in rows)
    if n<21:return {'C':max(dt,n*dt*10/183),'branch':'short'}
    ticks=pine_round((high-low)/tick);pos=(rows[0]['open']-low)/(high-low) if high>low else .5
    newh=rows[-1]['high']>max(r['high'] for r in rows[:-1]);newl=rows[-1]['low']<min(r['low'] for r in rows[:-1])
    ph=rows[-2]['high']>=rows[-3]['high'] and rows[-2]['high']>=rows[-1]['high']
    if pos<.25:
        C=pine_round(ticks*.786)+(4 if ph and not newh else 0);branch='root_pivot' if ph and not newh else 'root'
    elif ph and not newh:C=ticks+n;branch='pivot_add_count'
    elif newh or newl:C=pine_round(ticks*.786);branch='expansion'
    else:C=pine_round(ticks*.577)+(n-21)*2;branch='consolidation'
    return {'C':C,'branch':branch,'ticks':ticks,'start_position':pos,'new_high':newh,'new_low':newl,'previous_high_confirmed':ph}
def simulate(case,C):
    prefix=case['prefix'];suffix=case.get('suffixes',['c','d'])[-1]
    with (ROOT/'manual'/f'{prefix}_{suffix}.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))[:-1]
    end=max(int(r['time']) for r in case['OHLC']);endpoint=next(r for r in rows if int(r['time'])==end)
    high=case['high'];low=case['low'];dt=60
    alpha={k:2/((pine_round(base*C/dt) if k not in list(BASE)[:6] else base*C/dt)+1) for k,base in BASE.items()}
    bull={k:float(endpoint['low']) for k in BASE};bear={k:float(endpoint['high']) for k in BASE};side=None
    errors={'Lite':[],'Character':[]};visibility={'Lite':0,'Character':0}
    for r in rows:
        t=int(r['time'])
        if t<=end:continue
        if t>end+10800:break
        for k in BASE:
            bull[k]+=alpha[k]*(float(r['close'])-bull[k]);bear[k]+=alpha[k]*(float(r['close'])-bear[k])
        if side is None:
            if float(r['close'])>high:side='bull'
            elif float(r['close'])<low:side='bear'
        for k in BASE:
            family='Lite' if k.startswith('Lane') else 'Character'
            if bool(r[k])!=(side is not None):visibility[family]+=1
            if r[k] and side:
                errors[family].append(abs(float(r[k])-(bull if side=='bull' else bear)[k]))
    return {'supplied_C':C,'breakout_side':side,'families':{f:{'compared_values':len(es),'max_error':max(es,default=None),'visibility_mismatches':visibility[f]} for f,es in errors.items()}}
def main():
    raw=SOURCE.read_bytes();text=raw.decode('utf-8-sig')
    # Guard against silently auditing a subsequently changed formula.
    for token in ['ticks * 0.786','ticks * 0.577','bar_cnt - 21','start_pos < 0.25']:
        assert token in text,token
    digest=hashlib.sha256(raw).hexdigest();(ROOT/'pine/Gemini_hibrido_auditado.pine').write_bytes(raw)
    cases=[]
    for dataset in ['C_fronteras_nuevas.json','C_matriz.json','C_21_regimenes.json']:
        if not (ROOT/dataset).exists():continue
        d=json.loads((ROOT/dataset).read_text(encoding='utf-8-sig'))
        for c in d['cases']+d.get('shifts',[]):
            pred=predict(c['OHLC']);err=pred['C']-c['C']
            item={'dataset':dataset,'case':c.get('prefix',c['START']+'–'+c.get('END','')),'bars':c['bars'],'original_C':c['C'],'prediction':pred,'error_seconds':err,'match':abs(err)<1e-7}
            if dataset!='C_matriz.json':item['manual_engine']=simulate(c,c['C']);item['automatic_engine']=simulate(c,pred['C'])
            cases.append(item)
    out={'source_path':str(SOURCE),'sha256':digest,'tick_assumed_verified_NQ':.25,'scope':'Offline emulation of current Pine formulas and 180min causal state; not compilation or Pine runtime validation. Original source unchanged. Inputs equal native chart source, exact aligned anchors.','summary':{branch:{'cases':sum((c['bars']<21)==(branch=='short') for c in cases),'matches':sum(c['match'] and (c['bars']<21)==(branch=='short') for c in cases)} for branch in ['short','long']},'cases':cases}
    (ROOT/'Gemini_hibrido_auditoria.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'sha256':digest,'summary':out['summary'],'new_cases':[{k:v for k,v in c.items() if k not in ['manual_engine','automatic_engine']} for c in cases if c['dataset']=='C_fronteras_nuevas.json'],'manual_max_errors':{f:max(c['manual_engine']['families'][f]['max_error'] or 0 for c in cases if 'manual_engine'in c) for f in ['Lite','Character']},'manual_visibility_errors':sum(v['visibility_mismatches'] for c in cases if 'manual_engine'in c for v in c['manual_engine']['families'].values())},indent=2))
if __name__=='__main__':main()
