"""Preregistro del barrido START; interpolación local no es generador."""
import json
from analizar_C_fuente_vs_grafico import ROOT

def main():
    old=json.loads((ROOT/'C_rama24_resolucion_predicciones.json').read_text())
    base=next(c for c in old['cases'] if c['id']=='C_rama24_res_1903_45');cases=[]
    for removed,seconds in [(1,'15'),(2,'30'),(3,'45')]:
        rows=base['OHLC'][removed:]
        cases.append({'id':f'C_recorte1903_{seconds}','START':f'2026-10-12T19:03:{seconds}+00:00',
                      'END':base['END'],'dt':15,'bars':len(rows),'removed_bars':removed,
                      'predictions':{'linear_interpolation':88+(61-88)*removed/4},'OHLC':rows})
    out={'scope':'Locate local START transition88->61 across four removals. Only numerical candidate is linear interpolation fixed by known endpoints; predictions81.25,74.5,67.75 before measurement. It is not a general formula, and integer C alone is not used to pre-reject it. Diagnostic observations retain all failures. Counts and OHLC prefix change jointly.',
         'cases':cases}
    (ROOT/'C_recorte1903_predicciones.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in c.items() if k!='OHLC'} for c in cases],indent=2))

if __name__=='__main__':main()
