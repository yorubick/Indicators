"""Audita todas las columnas, incluidos glows y flags, antes de ruptura."""
import csv,json
from datetime import datetime,timezone
from analizar_C_fuente_vs_grafico import ROOT

def read(name):
    with (ROOT/'manual'/name).open(encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f);return r.fieldnames,list(r)

def utc(t):return datetime.fromtimestamp(int(t),timezone.utc).isoformat()

def main():
    _,refrows=read('Lite_1855_1920_1m_b.csv');ref={int(r['time']):r for r in refrows[:-1]}
    start=int(datetime.fromisoformat('2026-10-12T18:55:00+00:00').timestamp());end=start+25*60
    results=[]
    for tag in ['1924','step1','step2']:
        cols,a=read(f'C_prebreak_salidas_{tag}_a.csv');cols2,b=read(f'C_prebreak_salidas_{tag}_b.csv');assert cols==cols2
        aa={int(r['time']):r for r in a[:-1]};bb={int(r['time']):r for r in b[:-1]}
        common=sorted(set(aa)&set(bb));assert common
        assert all(aa[t][k]==bb[t][k] for t in common for k in cols)
        assert all(t in bb for t in range(start,end+1,60))
        assert all(bb[t][k]==ref[t][k] for t in bb if t in ref for k in ['open','high','low','close'])
        prices=[k for k in cols if k not in ['time','open','high','low','close','Volume','Bull delivery active','Bear delivery active']]
        assert len(prices)==26
        selected=[r for t,r in bb.items() if t>=end]
        assert selected and all(not r[k] for r in selected for k in prices)
        assert all(float(r[k])==0 for r in selected for k in ['Bull delivery active','Bear delivery active'])
        results.append({'tag':tag,'last_row_excluded':utc(b[-1]['time']),'last_closed_used':utc(b[-2]['time']),
                        'closed_rows_from_END':len(selected),'exported_columns':cols,'price_plot_columns':len(prices),
                        'nonempty_price_cells_from_END':0,'flags':'Bull/Bear delivery active both0',
                        'range_OHLC_complete':True,'reference_OHLC_agrees':True,'repeated_all_column_cells':len(common)*len(cols),
                        'C_observable_in_export':False})
    out={'START':utc(start),'END':utc(end),'date':'2026-10-12','source_and_chart_seconds':60,
         'sequence':'Initial cut19:24, then two Forward clicks, fixed anchors; last row always excluded.',
         'UI':'Inputs/Style audited Character6.5.36 and Lite1.2: no directC/table option. Data window at19:23:tenCharacterplots empty,flags0,Lite no additional scalarC.',
         'results':results,'conclusion':'No C observable before breakout in checked exported/UI outputs. Inconclusive on actual computation time and use of END-to-break bars. Empty plots and flags0 are not C0.'}
    (ROOT/'C_salidas_prebreak_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in r.items() if k!='exported_columns'} for r in results],indent=2))

if __name__=='__main__':main()
