"""Cruce de límites: hipótesis local congelada, no fórmula universal."""
import json
from analizar_C_fuente_vs_grafico import ROOT

def main():
    p=json.loads((ROOT/'C_recorte1903_predicciones.json').read_text());cases=[]
    for start,pred in [('15',67),('30',61)]:
        base=next(c for c in p['cases'] if c['START'][17:19]==start)
        rows=base['OHLC'][:-1]
        cases.append({'id':f'C_cruce1903_{start}','START':base['START'],
                      'END':'2026-10-12T19:23:30+00:00','dt':15,'bars':len(rows),
                      'prediction_C':pred,'OHLC':rows})
    out={'scope':'Local interaction model from known endpoints: if START still includes19:03:15, C67 before finalbar and88 after; if it excludes thatbar, C61 both before/after. Predicts67/61 for two new windows before measurement. Other properties and count change together; not proof of causal pivot detection or a general generator.', 'cases':cases}
    (ROOT/'C_cruce1903_predicciones.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in c.items() if k!='OHLC'} for c in cases],indent=2))

if __name__=='__main__':main()
