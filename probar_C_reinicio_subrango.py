"""Selección explícita y reinicio sin memoria anterior al evento."""
import json,sys,itertools
from analizar_C_fuente_vs_grafico import ROOT
from probar_C_selectores_pivotes import pivots

TYPES=[f'pivot_{side}_r{r}' for side in ['H','L'] for r in [1,2,3]]+['record_H','record_L','max_volume']+[f'volume_cross_{x}' for x in [1,1.5,2,3]]
SPEC={'event_types':TYPES,'choice':['first','last'],'reset_at':['event','confirmation'],
 'pivots':'Strict left, nonstrict right; wick source radius1/2/3, confirmation at i+radius within END.',
 'records':'Strict new global H/L sinceSTART, events only t>=1; confirmation same candle.',
 'max_volume':'First highest-volume candle within range; its position is the latest reset on strict running volume records including firstbar.',
 'volume_cross':'First EMA volume initialized with STARTvolume; previousEMA updated alpha2/21. Up-cross V_t>threshold*previousEMA and V_previous<=threshold*EMA_before_previous; t>=1. Confirmation same candle.',
 'descriptor':'dt,END,globalH/L,selectedevent side/type/absolute timestamp/OHLCV,entireOHLCV from reset throughEND. No totaln/START or state preceding reset.',
 'tests':'Identical descriptor/differentC refutes C=f(descriptor). Also test C=n*f(descriptor) permitting observedC+/-1; and C=K*selected_duration with commonK positive +/-1.',
 'scope':'Known overlapping9, no independent validation or training32. Reset forgets prefix except globalH/L. No collision does not prove a model; retained prefix-dependent seed or prehistory not excluded.'}

def events(rows,kind):
    if kind.startswith('pivot_'):
        _,side,r=kind.split('_');radius=int(r[1:])
        return [(i,i+radius) for i,s,p in pivots(rows,'wick',radius) if s==side]
    if kind=='max_volume':
        i=max(range(len(rows)),key=lambda i:rows[i]['volume']);return [(i,i)]
    if kind.startswith('record_'):
        key='high' if kind.endswith('H') else 'low';extreme=rows[0][key];out=[]
        for i,row in enumerate(rows[1:],1):
            v=row[key]
            if (v>extreme if key=='high' else v<extreme):out.append((i,i));extreme=v
        return out
    threshold=float(kind.split('_')[-1]);ema=rows[0]['volume'];prev_above=rows[0]['volume']>threshold*ema;out=[]
    for i,row in enumerate(rows[1:],1):
        above=row['volume']>threshold*ema
        if above and not prev_above:out.append((i,i))
        ema+=2/21*(row['volume']-ema);prev_above=above
    return out

def main():
    p=ROOT/'C_reinicio_subrango_preregistro.json'
    if '--spec' in sys.argv:p.write_text(json.dumps(SPEC,indent=2),encoding='utf-8');print('52 selectores congelados.');return
    assert json.loads(p.read_text())==SPEC
    cases=json.loads((ROOT/'C_matriz_frontera15s_volumen.json').read_text())['cases'];models=[]
    for kind,choice,at in itertools.product(TYPES,SPEC['choice'],SPEC['reset_at']):
        records=[];keys=[]
        for c in cases:
            rows=c['OHLC'];ev=events(rows,kind)
            if not ev:keys.append(None);records.append({'START':c['START'],'END':c['END'],'C':c['C'],'defined':False});continue
            i,confirm=ev[0 if choice=='first' else -1];start=i if at=='event' else confirm;selected=rows[start:]
            desc={'dt':c['dt'],'END':c['END'],'H':max(r['high'] for r in rows),'L':min(r['low'] for r in rows),
                  'event':rows[i],'selected':selected}
            keys.append(json.dumps(desc,sort_keys=True))
            records.append({'START':c['START'],'END':c['END'],'C':c['C'],'defined':True,'n':c['bars'],
                            'event_time':rows[i]['time'],'reset_time':rows[start]['time'],'selected_n':len(selected),
                            'duration_inclusive':len(selected)*c['dt']})
        witnesses=[];count=[]
        for i,j in itertools.combinations(range(len(cases)),2):
            if keys[i] is None or keys[i]!=keys[j]:continue
            a,b=records[i],records[j]
            if abs(a['C']-b['C'])>1e-7:witnesses.append({'A':a,'B':b})
            if max((a['C']-1)/a['n'],(b['C']-1)/b['n'])>min((a['C']+1)/a['n'],(b['C']+1)/b['n']):count.append({'A':a,'B':b})
        defined=[r for r in records if r['defined']]
        low=max((r['C']-1)/r['duration_inclusive'] for r in defined) if defined else None
        high=min((r['C']+1)/r['duration_inclusive'] for r in defined) if defined else None
        models.append({'event_type':kind,'choice':choice,'reset_at':at,'defined_cases':len(defined),
                       'descriptor_collisions':witnesses,'count_factor_collisions':count,
                       'duration_K_interval':[low,high],'duration_model_passes9':len(defined)==9 and low<=high,'cases':records})
    out={'spec':SPEC,'models':models,'model_count':len(models),
         'sole_descriptor_rejected':sum(bool(m['descriptor_collisions']) for m in models),
         'count_factor_rejected':sum(bool(m['count_factor_collisions']) for m in models),
         'duration_models_pass9':sum(m['duration_model_passes9'] for m in models),
         'training32_used':False,'reserved_validation_used':False}
    (ROOT/'C_reinicio_subrango_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ['spec','models']},indent=2))
    print(json.dumps([{'type':m['event_type'],'choice':m['choice'],'reset_at':m['reset_at'],'defined':m['defined_cases'],
                      'collisions':len(m['descriptor_collisions']),'count_collisions':len(m['count_factor_collisions']),
                      'duration_K':m['duration_K_interval']} for m in models if not m['descriptor_collisions']],indent=2))

if __name__=='__main__':main()
