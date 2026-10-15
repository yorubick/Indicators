"""Completa columna END:15 con dos predicciones locales previas."""
import json
from analizar_C_fuente_vs_grafico import ROOT

def main():
    p=json.loads((ROOT/'C_cruce1903_predicciones.json').read_text());cases=[]
    for c in p['cases']:
        rows=c['OHLC'][:-1];seconds=c['START'][17:19]
        cases.append({'id':f'C_cruce1915_{seconds}','START':c['START'],
                      'END':'2026-10-12T19:23:15+00:00','dt':15,'bars':len(rows),
                      'prediction_C':61,'OHLC':rows})
    out={'scope':'Local hypothesis: C61 at END19:23:15 persists for START19:03:15 and19:03:30, calibrated from known START19:03:00/END19:23:15. Predictions fixed before measurement. Not a general generator or independent episode replication.', 'cases':cases}
    (ROOT/'C_cruce1915_predicciones.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in c.items() if k!='OHLC'} for c in cases],indent=2))

if __name__=='__main__':main()
