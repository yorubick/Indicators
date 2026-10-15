"""Agrupa nueve selecciones verificadas; no modifica el dataset maestro."""
import json
from analizar_C_fuente_vs_grafico import ROOT,read
from lab_base_C import states

def main():
    wanted_start={'2026-10-12T19:03:'+x+'+00:00' for x in ['00','15','30']}
    wanted_end={'2026-10-12T19:23:'+x+'+00:00' for x in ['15','30','45']}
    grouped={}
    for tag in ['rama24_resolucion','transicion1923','recorte1903','cruce1903','cruce1915']:
        ps={c['id']:c for c in json.loads((ROOT/f'C_{tag}_predicciones.json').read_text())['cases']}
        for r in json.loads((ROOT/f'C_{tag}_resultados.json').read_text())['cases']:
            c=ps[r['id']]
            if c['START'] not in wanted_start or c['END'] not in wanted_end:continue
            key=(c['START'],c['END']);s=list(states(c['OHLC']))[-1]
            row={'START':c['START'],'END':c['END'],'dt':15,'bars':len(c['OHLC']),
                 'C':r['C'],'OHLC':c['OHLC'],'state':s,
                 'provenance':{'result':f'C_{tag}_resultados.json','id':c['id'],'pair':r['pair']}}
            if key in grouped:
                assert grouped[key]['OHLC']==row['OHLC'] and abs(grouped[key]['C']-row['C'])<1e-7
            grouped[key]=row
    assert len(grouped)==9
    source=read('Lite_185500_192200_15s_b.csv')
    for r in grouped.values():
        s=r['state'];end=r['OHLC'][-1]['time']
        r['first_break_after_END']=next(t for t in sorted(source) if t>end and
                                       (float(source[t]['close'])>s['high'] or float(source[t]['close'])<s['low']))
    out={'scope':'Nine overlapping verified selections from one episode, no independent validation. Separate from master93. Mandatory local counterexamples for candidate rules. No formula fitted.',
         'cases':[grouped[k] for k in sorted(grouped)]}
    (ROOT/'C_matriz_frontera15s.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ['START','END','bars','C','first_break_after_END']} for r in out['cases']],indent=2))

if __name__=='__main__':main()
