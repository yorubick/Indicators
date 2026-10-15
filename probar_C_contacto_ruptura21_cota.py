"""Robustez a cuantización: cota derivativa, no muestreo de raíces."""
import json,sys,itertools
from analizar_C_fuente_vs_grafico import ROOT
from probar_C_contacto_ruptura21 import FILES,FACTORS,read

SPEC={'base':'C_contacto_ruptura21_resultados.json','interval':'Underlying real C within measured C +/-1second.',
 'bound':'EMA convex recurrence alpha=2/(1+factor*C/dt). Across interval, abs(dEMA/dC)<=m*price_span*maxabs(dalpha/dC); max at C_lower. A contact root is impossible if abs(residual_at_C)>bound+1e-7.',
 'scope':'Conservative necessary condition only; failure to exclude is not a root. Additional audit registered after exact-contact result, no fit or validation.'}

def main():
    p=ROOT/'C_contacto_ruptura21_cota_preregistro.json'
    if '--spec' in sys.argv:p.write_text(json.dumps(SPEC,indent=2),encoding='utf-8');print('Cota cuantizacion registrada.');return
    assert json.loads(p.read_text())==SPEC
    base=json.loads((ROOT/SPEC['base']).read_text());cases=[c for c in json.loads((ROOT/'C_dataset_verificado.json').read_text())['cases'] if c['bars']==21 and c['split']=='training'];bounds={}
    for c in cases:
        data=read(FILES[c['id']][1]);end=c['OHLC'][-1];H=max(r['high'] for r in c['OHLC']);L=min(r['low'] for r in c['OHLC'])
        post=sorted([r for r in data if int(r['time'])>end['time']],key=lambda r:int(r['time']))
        first=next(r for r in post if float(r['close'])>H or float(r['close'])<L)
        seq=[r for r in post if int(r['time'])<=int(first['time'])]
        seed=end['low'] if float(first['close'])>H else end['high']
        for source,col in itertools.product(['close','hl2'],FACTORS):
            x=[float(r['close']) if source=='close' else (float(r['high'])+float(r['low']))/2 for r in seq]
            span=max([seed]+x)-min([seed]+x);q=FACTORS[col]/c['dt'];clo=c['C']-1
            assert 2/(1+q*clo)<=1
            bounds[c['id'],source,col]=len(seq)*span*2*q/(1+q*clo)**2
    models=[]
    for m in base['models']:
        rows=[]
        for r in m['cases']:
            b=bounds[r['id'],m['source'],m['curve']]
            rows.append({**r,'max_price_change_over_C_plusminus1':b,'contact_excluded':abs(r['residual'])>b+1e-7})
        models.append({'source':m['source'],'curve':m['curve'],'target':m['target'],'rejected_even_with_C_plusminus1':any(r['contact_excluded'] for r in rows),'cases':rows})
    out={'spec':SPEC,'model_count':len(models),'rejected':sum(m['rejected_even_with_C_plusminus1'] for m in models),'models':models,'reserved_validation_used':False}
    (ROOT/'C_contacto_ruptura21_cota_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ['spec','models']},indent=2))

if __name__=='__main__':main()
