"""Ajuste independiente de plots Lite y comparación con Character exportado."""
import csv,json,math,sys
from pathlib import Path
from identificar_emas import analyze,SOURCES
from obtener_C import recover
ROOT=Path(__file__).parent
LANES=['Lane 3 A','Lane 3 B','Lane 2 A','Lane 2 B','Lane 1 A','Lane 1 B']
def read(p):
    with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))[:-1]
def main():
    start=sys.argv[1] if len(sys.argv)>1 else '18:55:00'
    dt=int(sys.argv[2]) if len(sys.argv)>2 else 60
    end=sys.argv[3] if len(sys.argv)>3 else '19:20:00'
    date=sys.argv[4] if len(sys.argv)>4 else '2026-10-12'
    endtag=end.replace(':','') if end!='19:20:00' else '1920'
    resolution_tag={15:'15s',60:'1m',120:'2m'}[dt]
    prefix='Lite_'+(start.replace(':','') if dt!=60 else start[:5].replace(':',''))+'_'+endtag+'_'+resolution_tag
    if date!='2026-10-12':prefix='Lite_'+date.replace('-','')+'_'+prefix[5:]
    suffixes=sys.argv[5].split(',') if len(sys.argv)>5 else ['a','b']
    a=ROOT/'manual'/(prefix+'_'+suffixes[0]+'.csv');b=ROOT/'manual'/(prefix+'_'+suffixes[1]+'.csv')
    rows=read(b);other={int(r['time']):r for r in read(a)}
    closed=[r for r in rows[:-1] if int(r['time']) in other]
    assert all(r[k]==other[int(r['time'])][k] for r in closed for k in LANES), 'Plots Lite no repetidos'
    fits={}
    for col in LANES:
        candidates=[]
        for name,source in SOURCES.items():
            pairs=[(source(r)-float(p[col]),float(r[col])-float(p[col])) for p,r in zip(rows,rows[1:]) if p[col] and r[col] and int(r['time'])-int(p['time'])==dt]
            denom=sum(x*x for x,y in pairs)
            if not denom:continue
            alpha=sum(x*y for x,y in pairs)/denom
            candidates.append({'source':name,'period':2/alpha-1,'pairs':len(pairs),
                'rmse':math.sqrt(sum((y-alpha*x)**2 for x,y in pairs)/len(pairs))})
        assert candidates,col
        fits[col]=min(candidates,key=lambda v:v['rmse'])
    ct=analyze(b,dt);comparisons={}
    for lane in LANES:
        scores=[]
        for layer in ct['layers']:
            errors=[abs(float(r[lane])-float(r[layer])) for r in rows if r[lane] and r[layer]]
            if errors:scores.append({'layer':layer,'compared_values':len(errors),'max_error':max(errors),
                'RMSE_levels':math.sqrt(sum(e*e for e in errors)/len(errors)),
                'Character_period':ct['layers'][layer].get('period')})
        comparisons[lane]=min(scores,key=lambda v:v['RMSE_levels'])
    bases=dict(zip(LANES,[72/3,89/3,72/9,89/9,72/27,89/27]))
    C_values={lane:fits[lane]['period']*dt/bases[lane] for lane in LANES}
    out={'file':str(b),'chart_seconds':dt,'START_UTC':date+'T'+start+'Z','END_UTC':date+'T'+end+'Z',
        'Lite_source_seconds':dt,'Character_source':'Chart','Character_extraction':recover(b),
        'repeat_cells_compared':len(closed)*6,'Lite_fits':fits,'Lite_C_assuming_unrounded_family':C_values,'closest_Character_layers':comparisons,
        'scope':'Measured range; Lite source explicitly equal to chart. No assumption of shared C generator.'}
    (ROOT/(prefix+'_comparacion.json')).write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'Lite_fits':fits,'Lite_C':C_values,'Character_C':out['Character_extraction']['compatible_integer_C_seconds']},indent=2))
if __name__=='__main__':main()


