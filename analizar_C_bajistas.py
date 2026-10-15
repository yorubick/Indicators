"""Validación de nuevas parejas de CSV bajistas sin ajustar semilla a los plots."""
import csv,json
from pathlib import Path
from datetime import datetime,timezone
from obtener_C import recover
from flujo_manual import FlujoManual
ROOT=Path(__file__).parent
def stamp(t):return int(datetime.fromisoformat('2026-10-12T'+t+':00+00:00').timestamp())
def utc(t):return datetime.fromtimestamp(t,timezone.utc).isoformat() if t else None

def main():
    results=[]
    for start,end in [('04:45','05:15'),('04:45','05:25'),('04:45','05:30'),('04:50','05:25')]:
        prefix=f'C_bear_{start.replace(":","")}_{end.replace(":","")}'
        a,b=ROOT/(prefix+'_a.csv'),ROOT/(prefix+'_b.csv')
        if not a.exists() or not b.exists():continue
        x,y=recover(a),recover(b);assert x['periods']==y['periods'],prefix
        ra={int(r['time']):r for r in csv.DictReader(a.open(encoding='utf-8-sig'))}
        rb={int(r['time']):r for r in csv.DictReader(b.open(encoding='utf-8-sig'))}
        common=sorted(set(ra)&set(rb))[:-2]
        assert all(ra[t][k]==rb[t][k] for t in common for k in x['periods']),prefix
        s,e=stamp(start),stamp(end);needed=list(range(s,e+5401,60))
        assert all(t in rb for t in needed),prefix
        seg=[rb[t] for t in range(s,e+1,60)]
        high=max(float(r['high']) for r in seg);low=min(float(r['low']) for r in seg)
        C=y['compatible_integer_C_seconds'];assert len(C)==1
        end_high=float(rb[e]['high']);end_low=float(rb[e]['low'])
        flow=FlujoManual(C[0],60,high,low,end_high,end_low)
        assert flow.periods==y['periods']
        errors=[];breaktime=None;plotstart=None;before=0;missing=0
        for t in range(e+60,e+5401,60):
            r=rb[t];prediction=flow.closed_bar_after_END(float(r['close']))
            if prediction is not None and breaktime is None:breaktime=t
            for k in flow.periods:
                if r[k]:
                    if plotstart is None:plotstart=t
                    if prediction is None:before+=1
                    else:errors.append(abs(float(r[k])-prediction[k]))
                elif prediction is not None:missing+=1
        result={'start':start,'end':end,'source_seconds':60,'extraction':y,
            'repeat_file':str(a),'repeated_common_values':len(common)*10,'range_high':high,'range_low':low,
            'END_high':end_high,'END_low':end_low,'chosen_direction':flow.side,
            'first_breakout_UTC':utc(breaktime),'first_plot_UTC':utc(plotstart),
            'values_compared':len(errors),'max_error':max(errors) if errors else None,
            'unexpected_plots_before_breakout':before,'missing_plots_after_breakout':missing,
            'matches':len(errors)>=50 and before==0 and missing==0 and max(errors)<1e-8}
        results.append(result)
    out={'cases':results,'matching_count':sum(c['matches'] for c in results),
         'scope':'NQ1!, Manual profile B, source=chart 1m, same date with overlapping ranges. C recovered from original plots; dual-branch simulation receives C but never fits seed from plots. First 90min after END.'}
    (ROOT/'C_bajistas.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
