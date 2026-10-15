"""Prueba de suficiencia de entradas por extremos de dos mitades.

No ajusta C: si las entradas son idénticas yCdiffiere, ningún mapeo
determinista de esas entradas puede explicar ambos casos.
"""
import json,math,sys
from analizar_C_fuente_vs_grafico import ROOT

SPEC={'inputs':'dt,n,half lengths and high/low of each half, full high/low',
      'sources':['wick','close'],'odd_split':['floor','ceil'],
      'candidate_statistic':'Q=(R1/n1+R2/n2)/(R/n), D=log2(Q) if all widths positive.',
      'gate':'Exact descriptor collision with differentC rejects any function solely of these inputs, including any rounding or shared adaptive exponent. No fitted constants.',
      'scope':'Final-window half extrema only; does not cover rolling histories, recursive state, additional sources/volume or inputs outsideSTART..END. Nine overlapping known cases, no validation.'}

def describe(c,source,split):
    rows=c['OHLC'];n=len(rows);cut=n//2 if split=='floor' else (n+1)//2
    def extrema(r):
        return (max(x['high'] for x in r),min(x['low'] for x in r)) if source=='wick' else (max(x['close'] for x in r),min(x['close'] for x in r))
    H,L=extrema(rows);H1,L1=extrema(rows[:cut]);H2,L2=extrema(rows[cut:])
    inputs={'dt':c['dt'],'n':n,'n1':cut,'n2':n-cut,'H':H,'L':L,'H1':H1,'L1':L1,'H2':H2,'L2':L2}
    widths=[H-L,H1-L1,H2-L2]
    Q=((H1-L1)/cut+(H2-L2)/(n-cut))/((H-L)/n) if all(w>0 for w in widths) else None
    return inputs,{'Q':Q,'D':math.log2(Q) if Q else None}

def main():
    if '--spec' in sys.argv:
        (ROOT/'C_rangos_mitades_preregistro.json').write_text(json.dumps(SPEC,indent=2),encoding='utf-8')
        print(json.dumps(SPEC,indent=2));return
    assert json.loads((ROOT/'C_rangos_mitades_preregistro.json').read_text())==SPEC
    cases=json.loads((ROOT/'C_matriz_frontera15s.json').read_text())['cases'];models=[]
    for source in SPEC['sources']:
        for split in SPEC['odd_split']:
            groups={};rows=[]
            for c in cases:
                d,f=describe(c,source,split);row={'START':c['START'],'END':c['END'],'C':c['C'],'inputs':d,'statistics':f}
                rows.append(row);groups.setdefault(tuple(d.values()),[]).append(row)
            pairs=[]
            for g in groups.values():
                for i,a in enumerate(g):
                    for b in g[i+1:]:
                        if abs(a['C']-b['C'])>1e-7:pairs.append({'inputs':a['inputs'],'case_A':{k:a[k] for k in ['START','END','C']},'case_B':{k:b[k] for k in ['START','END','C']}})
            models.append({'source':source,'split':split,'distinct_descriptors':len(groups),'contradictory_pairs':pairs,'cases':rows})
    out={'spec':SPEC,'models':models,'rejected_signatures':sum(bool(m['contradictory_pairs']) for m in models),'training32_used':False,'reserved_validation_used':False}
    (ROOT/'C_rangos_mitades_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'rejected_signatures':out['rejected_signatures'],'models':[{'source':m['source'],'split':m['split'],'distinct_descriptors':m['distinct_descriptors'],'contradictory_pair_count':len(m['contradictory_pairs']),'first_counterexample':m['contradictory_pairs'][:1]} for m in models]},indent=2))

if __name__=='__main__':main()
