"""Contraste directo de END nativo frente a la última subvela del gráfico."""
import json,datetime
from analizar_C_fuente_vs_grafico import ROOT,LANES,read,fit_lite,fit_four_steps

def stamp(t):return datetime.datetime.fromtimestamp(t,datetime.timezone.utc).isoformat()
def reconstruct(native,coarse,endpoint,C,step,startpoint='2026-10-12T18:55:00+00:00'):
    end=int(datetime.datetime.fromisoformat(endpoint).timestamp());seed=float(coarse[end-(step-15)]['low'])
    start=int(datetime.datetime.fromisoformat(startpoint).timestamp())
    window=[r for t,r in native.items() if start<=t<=end]
    high=max(float(r['high']) for r in window);low=min(float(r['low']) for r in window)
    published=False;first_break=None;visibility=[]
    bases=[24,89/3,8,89/9,72/27,89/27];ys={col:seed for col in LANES}
    errors={col:[] for col in LANES}
    for t,r in native.items():
        if t<=end:continue
        if not published and (float(r['close'])>high or float(r['close'])<low):
            published=True;first_break={'time':stamp(t),'side':'bull' if float(r['close'])>high else 'bear'}
        for col,base in zip(LANES,bases):ys[col]+=2/(base*C/15+1)*(float(r['close'])-ys[col])
        coarse_t=t-(step-15)
        if coarse_t in coarse:
            for col in LANES:
                if bool(coarse[coarse_t][col])!=published:visibility.append({'time':stamp(coarse_t),'column':col})
                if coarse[coarse_t][col]:errors[col].append(abs(ys[col]-float(coarse[coarse_t][col])))
    return {'seed':seed,'END_native':endpoint,'C_supplied':C,'range_high':high,'range_low':low,'first_break':first_break,'visibility_mismatches_after_END':visibility,'curves':{col:{'values':len(es),'max_error':max(es,default=None)} for col,es in errors.items()}}
def compare_lite(native,other,offset):
    out={};vis=[]
    for col in LANES:
        errors=[]
        for t,r in other.items():
            if t+offset not in native:continue
            p=native[t+offset]
            if bool(r[col])!=bool(p[col]):vis.append({'time':stamp(t),'column':col})
            if r[col] and p[col]:errors.append(abs(float(r[col])-float(p[col])))
        out[col]={'values':len(errors),'max_error':max(errors,default=None)}
    return {'offset_seconds':offset,'visibility_mismatches':vis,'curves':out}
def main():
    out={}
    for end,chart,expected in [('192015',30,79),('192045',60,66)]:
        a=read(f'Lite_END_{end}_a.csv');b=read(f'Lite_END_{end}_b.csv')
        coarse=read('C_source15_chart30_b.csv' if chart==30 else 'C_source15_chart60_d.csv')
        out[end]={'expected_C':expected,'fits':fit_lite(b),'repeat':compare_lite(a,b,0),'coarse_chart_seconds':chart,'coarse_comparison':compare_lite(b,coarse,chart-15),'first_native_plot':stamp(next(t for t,r in b.items() if r[LANES[0]])),'first_coarse_plot':stamp(next(t for t,r in coarse.items() if r[LANES[0]]))}
        out[end]['coarse_chart_low_seed_reconstruction']=reconstruct(b,coarse,'2026-10-12T19:20:'+('15' if chart==30 else '45')+'+00:00',expected,chart)
    if (ROOT/'manual/Lite_minuto21_END45_b.csv').exists():
        native=read('Lite_minuto21_END45_b.csv');coarse=read('Lite_minuto21_chart60_b.csv')
        out['minute21_control']={'native_fits':fit_lite(native),'coarse_independent_C_fits':fit_four_steps(native,coarse,60),'native_repeat':compare_lite(read('Lite_minuto21_END45_a.csv'),native,0),'coarse_repeat':compare_lite(read('Lite_minuto21_chart60_a.csv'),coarse,0),'comparison':compare_lite(native,coarse,45),'seed_reconstruction':reconstruct(native,coarse,'2026-10-12T19:21:45+00:00',66,60)}
    (ROOT/'Lite_END_efectivo.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
