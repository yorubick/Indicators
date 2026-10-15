"""Cortes de replay: pares Lite cerrados, repetición y referencia histórica."""
import csv,json,math
from pathlib import Path
from datetime import datetime,timezone
from obtener_C import recover
ROOT=Path(__file__).parent
LANES=['Lane 3 A','Lane 3 B','Lane 2 A','Lane 2 B','Lane 1 A','Lane 1 B']
LAYERS=['Layer A','Layer A boundary','Layer B','Layer B boundary','Layer C','Layer C boundary',
        'Extra cloud 1','Extra cloud 1 boundary','Extra cloud 2','Extra cloud 2 boundary']
BASES=dict(zip(LANES,[72/3,89/3,72/9,89/9,72/27,89/27]))
def read(p):
    with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def utc(t):return datetime.fromtimestamp(int(t),timezone.utc).isoformat()
def main():
    reference={int(r['time']):r for r in read(ROOT/'manual'/'Lite_1855_1920_1m_b.csv')[:-1]}
    results=[]
    for cut in ('1925','1929','1933','1940'):
        prefix=ROOT/'manual'/('C_observabilidad_'+cut)
        suffixes=('a','b') if cut=='1925' else ('c','d')
        a,b=[read(Path(str(prefix)+'_'+s+'.csv')) for s in suffixes]
        other={int(r['time']):r for r in a[:-1]};closed=b[:-1]
        common=[r for r in closed if int(r['time']) in other]
        assert common
        assert all(r[k]==other[int(r['time'])][k] for r in common for k in LANES+LAYERS),cut
        comparable=[r for r in closed if int(r['time']) in reference]
        mismatches=[(utc(r['time']),k) for r in comparable for k in LANES+LAYERS if r[k]!=reference[int(r['time'])][k]]
        ohlc_mismatches=[(utc(r['time']),k) for r in comparable for k in ('open','high','low','close') if float(r[k])!=float(reference[int(r['time'])][k])]
        fits={}
        for lane in LANES:
            pairs=[(float(r['close'])-float(p[lane]),float(r[lane])-float(p[lane])) for p,r in zip(closed,closed[1:])
                   if p[lane] and r[lane] and int(r['time'])-int(p['time'])==60]
            if not pairs:continue
            denominator=sum(x*x for x,y in pairs)
            if denominator<=1e-10:continue
            alpha=sum(x*y for x,y in pairs)/denominator
            N=2/alpha-1
            fits[lane]={'pairs':len(pairs),'denominator':denominator,'N':N,'C':N*60/BASES[lane],
                        'rmse':math.sqrt(sum((y-alpha*x)**2 for x,y in pairs)/len(pairs))}
        try:ct=recover(Path(str(prefix)+'_'+suffixes[1]+'.csv'))
        except (Exception, SystemExit) as exc:ct={'not_extracted':str(exc)}
        last=b[-1];last_matches_previous=all(last[k]==reference.get(int(last['time'])-60,{}).get(k) for k in LANES+LAYERS)
        start=int(datetime.fromisoformat('2026-10-12T18:55:00+00:00').timestamp());end=start+25*60
        available={int(r['time']) for r in closed}
        results.append({'cut_requested':cut,'file':str(Path(str(prefix)+'_'+suffixes[1]+'.csv')),
            'last_row_UTC':utc(last['time']),'last_included_row_UTC':utc(closed[-1]['time']),
            'range_OHLC_complete':all(t in available for t in range(start,end+1,60)),
            'repeated_plot_cells':len(common)*16,'reference_nonempty_plot_cells':sum(bool(r[k]) for r in comparable for k in LANES+LAYERS),
            'plot_mismatches':mismatches,'OHLC_mismatches':ohlc_mismatches,
            'Lite_C_observable':len(fits)==6,'Lite_fits':fits,'Character_extraction':ct,
            'excluded_last_row_matches_previous_reference_plots':last_matches_previous})
    out={'START':'2026-10-12T18:55:00Z','END':'2026-10-12T19:20:00Z','chart_seconds':60,
         'Lite_source':'explicit 1m','Character_source':'Chart','results':results,
         'scope':'One bullish range. First fit has one pair per curve: zero regression residual is tautological there; use agreement of six C estimates, repeated exports and exact historical levels as corroboration. Does not exclude END-to-breakout data.'}
    (ROOT/'C_observabilidad.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{'cut':r['cut_requested'],'last':r['last_row_UTC'],'complete_range':r['range_OHLC_complete'],
       'Lite_C':[f['C'] for f in r['Lite_fits'].values()],'pairs':[f['pairs'] for f in r['Lite_fits'].values()],
       'nonempty_reference_cells':r['reference_nonempty_plot_cells'],'mismatches':len(r['plot_mismatches']),
       'OHLC_mismatches':len(r['OHLC_mismatches']),'last_lag':r['excluded_last_row_matches_previous_reference_plots']} for r in results],indent=2))
if __name__=='__main__':main()
