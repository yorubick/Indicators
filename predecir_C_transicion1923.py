"""Dos discriminadores locales congelados antes de medir END15/30."""
import json
from lab_base_C import states
from analizar_C_fuente_vs_grafico import ROOT

def main():
    p=json.loads((ROOT/'C_rama24_resolucion_predicciones.json').read_text())
    base=next(c for c in p['cases'] if c['id']=='C_rama24_res_1903_45');hist=list(states(base['OHLC']));cases=[]
    for second,n in [('15',82),('30',83)]:
        bars=base['OHLC'][:n];s=hist[n-1];prev=hist[n-2];r=bars[-1]
        events={'new_high':s['new_high'],'new_low':s['new_low'],
                'confirmed_high':s['last_confirmed_high']!=prev['last_confirmed_high'],
                'confirmed_low':s['last_confirmed_low']!=prev['last_confirmed_low']}
        cases.append({'id':f'C_transicion1923_{second}','START':base['START'],
                      'END':f'2026-10-12T19:23:{second}+00:00','dt':15,'bars':n,'OHLC':bars,
                      'events':events,'END_body':r['close']-r['open'],
                      'predictions':{'confirmed_low_switch':88 if events['confirmed_low'] else 67,
                                     'red_END_body_switch':88 if r['close']<r['open'] else 67}})
    out={'scope':'Two local endpoint-calibrated discriminators, not general C formulas. Known START19:03 END00 C67 and END45 C88. Model1: new radius1 low pivot at END selects88, otherwise67. Model2: red END body selects88, otherwise67. Freeze before new C measurements. General event necessity was already refuted; this test only distinguishes local explanations.', 'cases':cases}
    (ROOT/'C_transicion1923_predicciones.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in c.items() if k!='OHLC'} for c in cases],indent=2))

if __name__=='__main__':main()
