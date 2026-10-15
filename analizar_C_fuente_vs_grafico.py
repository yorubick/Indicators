"""Compara fuentes 15s explícitas con dos intervalos de gráfico; sin ajustar EMA a OHLC agregado."""
import csv,json,math,datetime
from pathlib import Path
from obtener_C import recover,BASE
ROOT=Path(__file__).parent
LANES=['Lane 3 A','Lane 3 B','Lane 2 A','Lane 2 B','Lane 1 A','Lane 1 B']
COLS=LANES+list(BASE)
def read(name):
    with (ROOT/'manual'/name).open(encoding='utf-8-sig') as f:
        return {int(r['time']):r for r in list(csv.DictReader(f))[:-1]}
def compare(a,b,offset=0):
    errors={k:[] for k in COLS}; visibility=0
    for t,r in b.items():
        if t+offset not in a:continue
        p=a[t+offset]
        for k in COLS:
            if bool(r[k])!=bool(p[k]):visibility+=1
            if r[k] and p[k]:errors[k].append(abs(float(r[k])-float(p[k])))
    return {'offset_seconds':offset,'visibility_mismatches':visibility,'curves':{k:{'values':len(es),'max_error':max(es,default=None)} for k,es in errors.items()}}
def fit_lite(rows,step=15,period_seconds=15):
    out={}
    for col,base in zip(LANES,[24,89/3,8,89/9,72/27,89/27]):
        pairs=[(float(r['close'])-float(rows[t-step][col]),float(r[col])-float(rows[t-step][col])) for t,r in rows.items() if t-step in rows and r[col] and rows[t-step][col]]
        alpha=sum(x*y for x,y in pairs)/sum(x*x for x,y in pairs)
        out[col]={'C':(2/alpha-1)*period_seconds/base,'period':2/alpha-1,'pairs':len(pairs),'rmse':math.sqrt(sum((y-alpha*x)**2 for x,y in pairs)/len(pairs))}
    return out
def fit_character_samples(native,coarse,step,periods):
    result={}
    for col,N in periods.items():
        errors=[]
        for t,r in coarse.items():
            if t-step not in coarse or not r[col] or not coarse[t-step][col]:continue
            stamps=list(range(t,t+step,15))
            if not all(s in native for s in stamps):continue
            y=float(coarse[t-step][col]);alpha=2/(N+1)
            for s in stamps:y+=alpha*(float(native[s]['close'])-y)
            errors.append(abs(y-float(r[col])))
        result[col]={'fixed_native_period':N,'pairs':len(errors),'max_error':max(errors),'rmse':math.sqrt(sum(e*e for e in errors)/len(errors))}
    return result
def fit_four_steps(native,coarse,step=60,columns=LANES):
    """Ajusta actualizaciones nativas entre muestras agregadas con OHLC 15s observado."""
    result={}
    for col in columns:
        base=dict(zip(LANES,[24,89/3,8,89/9,72/27,89/27])).get(col,BASE.get(col))
        pairs=[]
        for t,r in coarse.items():
            if t-step not in coarse or not r[col] or not coarse[t-step][col]:continue
            stamps=[t+k for k in range(0,step,15)]
            if not all(s in native for s in stamps):continue
            pairs.append((float(coarse[t-step][col]),float(r[col]),[float(native[s]['close']) for s in stamps]))
        def score(C):
            alpha=2/(base*C/15+1);se=0
            for prev,target,closes in pairs:
                y=prev
                for close in closes:y+=alpha*(close-y)
                se+=(y-target)**2
            return se/len(pairs)
        lo,hi=1.,300.
        for _ in range(100):
            a=lo+(hi-lo)/3;b=hi-(hi-lo)/3
            if score(a)<score(b):hi=b
            else:lo=a
        C=(lo+hi)/2
        result[col]={'C':C,'pairs':len(pairs),'rmse':math.sqrt(score(C))}
    return result
def main():
    native=read('C_source15_chart15_antes_b.csv');coarse=read('C_source15_chart60_d.csv')
    out={'configuration':{'source_seconds_both':15,'START':'2026-10-12T18:55:00Z','END':'2026-10-12T19:20:00Z'},'native_Character':recover(ROOT/'manual/C_source15_chart15_antes_b.csv'),'native_Lite':fit_lite(native),'native_repeat':compare(read('C_source15_chart15_antes_a.csv'),native),'coarse_repeat':compare(read('C_source15_chart60_c.csv'),coarse),'predeclared_mappings':[compare(native,coarse,k) for k in [45,0,15,30]],'exploratory_coarse_Lite_chart_close_fit_using_15s_period_scale':fit_lite(coarse,60,15)}
    ret=ROOT/'manual/C_source15_chart15_regreso_b.csv'
    if ret.exists():
        back=read(ret.name);out['return_Character']=recover(ret);out['return_Lite']=fit_lite(back);out['roundtrip']=compare(native,back);out['return_repeat']=compare(read('C_source15_chart15_regreso_a.csv'),back)
    out['exploratory_coarse_Lite_four_native_updates']=fit_four_steps(native,coarse)
    out['Character_fixed_C106_recurrence_chart60']=fit_character_samples(native,coarse,60,out['native_Character']['periods'])
    half=ROOT/'manual/C_source15_chart30_b.csv'
    if half.exists():
        halfrows=read(half.name)
        out['predeclared_control30']={'repeat':compare(read('C_source15_chart30_a.csv'),halfrows),'mapping':compare(native,halfrows,15),'Lite_two_native_updates':fit_four_steps(native,halfrows,30)}
        out['predeclared_control30']['Character_fixed_C106_recurrence']=fit_character_samples(native,halfrows,30,out['native_Character']['periods'])
    # Diagnóstico posterior, conservando también el resultado completo con sus errores.
    lo=int(datetime.datetime(2026,10,12,19,20,tzinfo=datetime.timezone.utc).timestamp());hi=lo+5400
    out['posthoc_first90_minutes']={}
    for step,data in [(60,coarse),(30,read('C_source15_chart30_b.csv'))]:
        scoped={t:r for t,r in data.items() if lo<=t<hi}
        out['posthoc_first90_minutes'][str(step)]={'scope':'19:20–20:50 UTC, definido después de ver discrepancias completas; no reemplaza prueba completa','Character_recurrence':fit_character_samples(native,scoped,step,out['native_Character']['periods']),'mapping':compare(native,scoped,step-15)}
    (ROOT/'C_fuente_vs_grafico.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
