import csv,json,math
from pathlib import Path
from datetime import datetime,timezone
from comparar_Lite_Character import LANES
ROOT=Path(__file__).parent
LAYERS=['Layer A','Layer A boundary','Layer B','Layer B boundary','Layer C','Layer C boundary','Extra cloud 1','Extra cloud 1 boundary','Extra cloud 2','Extra cloud 2 boundary']
BASES=dict(zip(LANES,[72/3,89/3,72/9,89/9,72/27,89/27]))
def read(p):
    with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def utc(t):return datetime.fromtimestamp(int(t),timezone.utc).isoformat()
def main():
    reference={int(r['time']):r for r in read(ROOT/'manual'/'Lite_1904_192800_1m_b.csv')[:-1]}
    results=[];accepted={}
    for mode in ('directo','antes_END','secuencial'):
        a,b=[read(ROOT/'manual'/('C_replay128_'+mode+'_'+s+'.csv')) for s in ('a','b')]
        rows=b[:-1];ad={int(r['time']):r for r in a[:-1]};common=[r for r in rows if int(r['time']) in ad]
        assert common and all(r[k]==ad[int(r['time'])][k] for r in common for k in LANES+LAYERS),mode
        comparable=[r for r in rows if int(r['time']) in reference]
        differences=[(r['time'],k) for r in comparable for k in LANES+LAYERS if r[k]!=reference[int(r['time'])][k]]
        price_differences=[(r['time'],k) for r in comparable for k in ('open','high','low','close') if float(r[k])!=float(reference[int(r['time'])][k])]
        fits={}
        for lane in LANES:
            pairs=[(float(r['close'])-float(p[lane]),float(r[lane])-float(p[lane])) for p,r in zip(rows,rows[1:]) if p[lane] and r[lane] and int(r['time'])-int(p['time'])==60]
            if not pairs:continue
            denom=sum(x*x for x,y in pairs);alpha=sum(x*y for x,y in pairs)/denom
            fits[lane]={'pairs':len(pairs),'denominator':denom,'C':(2/alpha-1)*60/BASES[lane]}
        accepted[mode]={int(r['time']):r for r in rows}
        results.append({'mode':mode,'last_exported':utc(b[-1]['time']),'last_included':utc(rows[-1]['time']),
          'fits_Lite':fits,'historical_plot_differences':differences,'historical_OHLC_differences':price_differences,
          'nonempty_historical_plot_cells_compared':sum(bool(r[k]) for r in comparable for k in LANES+LAYERS)})
    timestamps=set(accepted['directo'])&set(accepted['secuencial'])
    mode_differences=[(t,k) for t in sorted(timestamps) for k in LANES+LAYERS if accepted['directo'][t][k]!=accepted['secuencial'][t][k]]
    out={'START':'2026-10-12T19:04:00Z','END':'2026-10-12T19:28:00Z','dt':60,
       'results':results,'direct_vs_sequential_plot_differences':mode_differences,
       'scope':'One case C128. Direct replay select19:32 versus select19:28 plus four forward steps. Exclude last row; one pair per Lite curve is not a residual validation. Agreement with full-history levels and repeated exports corroborates. Does not exclude END-to-breakout or internal-series effects.'}
    (ROOT/'C_replay128.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
