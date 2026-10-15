"""Preregistro: END fijo, extensión y recorte simétricos de START."""
import json,datetime
from analizar_C_fuente_vs_grafico import ROOT,read
from lab_base_C import states

def descriptor(rows):
    s=list(states(rows))[-1];n=s['n']
    return {'H':s['high'],'L':s['low'],'END_close':s['close'],
            'age_H':n-1-s['idx_high'],'age_L':n-1-s['idx_low'],
            'age_pivot_H':n-1-s['last_confirmed_high'],
            'age_pivot_L':n-1-s['last_confirmed_low']}

def main():
    source=read('Lite_185500_192200_15s_b.csv')
    old=json.loads((ROOT/'C_rama24_resolucion_predicciones.json').read_text())
    base=next(c for c in old['cases'] if c['id']=='C_rama24_res_1903_45')
    desc=descriptor(base['OHLC']);END=base['OHLC'][-1]['time'];cases=[]
    for start in ['19:02','19:04']:
        START=int(datetime.datetime.fromisoformat(f'2026-10-12T{start}:00+00:00').timestamp())
        rows=[{'time':t,**{k:float(source[t][k]) for k in ['open','high','low','close']}} for t in range(START,END+1,15)]
        d=descriptor(rows)
        assert d==desc and rows[-21:]==base['OHLC'][-21:]
        cases.append({'id':f'C_prefijo192345_{start.replace(":","")}',
                      'START':f'2026-10-12T{start}:00+00:00','END':base['END'],'dt':15,
                      'bars':len(rows),'prediction_C':88,'preserved_descriptor':d,
                      'last21_exact':True,'OHLC':rows})
    out={'scope':'Local sufficiency hypothesis: unchanged H/L, extreme ages, radius1 pivot ages, ENDclose and last21OHLC imply sameC88 as observed START19:03. n and prefix differ together, so failure does not isolate which is causal. Prior broader suffix hypotheses failed; no general generator asserted.',
         'baseline':{'START':base['START'],'END':base['END'],'bars':84,'C':88,'descriptor':desc},'cases':cases}
    (ROOT/'C_prefijo192345_predicciones.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({**out,'cases':[{k:v for k,v in c.items() if k!='OHLC'} for c in cases]},indent=2))

if __name__=='__main__':main()
