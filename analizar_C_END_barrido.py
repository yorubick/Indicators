"""Barrido de END repetido; descriptores fijados sin ajustar reglas por caso."""
import csv,json
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).parent
from obtener_C import recover
def stamp(t):return int(datetime.fromisoformat('2026-10-12T'+t+'+00:00').timestamp())
def read(p):
    with p.open(encoding='utf-8-sig') as f:return {int(r['time']):r for r in list(csv.DictReader(f))[:-1]}
def main():
    cases=[];previous=None
    for end in ('19:21:00','19:21:15','19:21:30','19:21:45','19:22:00'):
        prefix=ROOT/'manual'/('C_END_'+end.replace(':',''));a=Path(str(prefix)+'_a.csv');b=Path(str(prefix)+'_b.csv')
        x,y=recover(a),recover(b);assert x['periods']==y['periods'],end
        ra,rb=read(a),read(b);common=sorted(set(ra)&set(rb))[:-1]
        assert all(ra[t][k]==rb[t][k] for t in common for k in y['periods']),end
        ts=list(range(stamp('18:55:00'),stamp(end)+1,15));assert all(t in rb for t in ts)
        values=[{k:float(rb[t][k]) for k in ('open','high','low','close')} for t in ts]
        if previous:assert values[:-1]==previous
        h=max(v['high'] for v in values);l=min(v['low'] for v in values);last=values[-1]
        closes=[v['close'] for v in values];diff=[b-a for a,b in zip(closes,closes[1:])]
        nz=[d for d in diff if d]
        case={'END_UTC':end,'C':y['compatible_integer_C_seconds'][0],'extraction':y,'bars':len(values),
            'END_OHLC':last,'range_high':h,'range_low':l,
            'new_global_high':last['high']>max(v['high'] for v in values[:-1]),
            'new_global_low':last['low']<min(v['low'] for v in values[:-1]),
            'END_body':last['close']-last['open'],'last_close_change':diff[-1],
            'close_reversal_at_END':diff[-1]!=0 and len(nz)>=2 and nz[-1]*nz[-2]<0,
            'close_total_variation':sum(abs(d) for d in diff),
            'closed_common_plot_cells_compared':len(common)*10}
        if cases:case['C_change']=case['C']-cases[-1]['C']
        cases.append(case);previous=values
    out={'cases':cases,'scope':'Same date overlapping windows, Manual profile B chart/source15s. C from original plots. No generator inferred. All new pairs repeat exactly.'}
    (ROOT/'C_END_barrido.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in c.items() if k!='extraction'} for c in cases],indent=2))
if __name__=='__main__':main()
