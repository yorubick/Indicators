import csv,json
from pathlib import Path
from datetime import datetime
from comparar_Lite_Character import LANES
ROOT=Path(__file__).parent
LAYERS=['Layer A','Layer A boundary','Layer B','Layer B boundary','Layer C','Layer C boundary','Extra cloud 1','Extra cloud 1 boundary','Extra cloud 2','Extra cloud 2 boundary']
def read(p):
    with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))[:-1]
def stamp(t):return int(datetime.fromisoformat('2026-10-12T'+t+'+00:00').timestamp())
def main():
    results=[]
    for start,end in [('19:00:00','19:'+m+':00') for m in ('01','02','03','07','11','15','16','17','18','19','20')]+[('19:01:00','19:18:00')]:
        endtag=end.replace(':','') if end!='19:20:00' else '1920'
        prefix='Lite_'+start[:5].replace(':','')+'_'+endtag+'_1m'
        j=json.loads((ROOT/(prefix+'_comparacion.json')).read_text(encoding='utf-8-sig'))
        a=read(ROOT/'manual'/(prefix+'_a.csv'));b=read(ROOT/'manual'/(prefix+'_b.csv'));ad={int(r['time']):r for r in a}
        common=[r for r in b if int(r['time']) in ad]
        assert common and all(r[k]==ad[int(r['time'])][k] for r in common for k in LANES+LAYERS),prefix
        selected=[r for r in b if stamp(start)<=int(r['time'])<=stamp(end)]
        assert [int(r['time']) for r in selected]==list(range(stamp(start),stamp(end)+1,60)),prefix
        cs=list(j['Lite_C_assuming_unrounded_family'].values());C=sum(cs)/6
        interval=j['Character_extraction']['C_seconds_interval']
        assert max(cs)-min(cs)<1e-8
        assert interval['lower_inclusive']<=C<interval['upper_exclusive'],prefix
        results.append({'START':start,'END':end,'bars':len(selected),'Lite_C':C,'six_C_spread':max(cs)-min(cs),
            'Character_C_interval':interval,'compatible_integer_C':j['Character_extraction']['compatible_integer_C_seconds'],
            'high':max(float(r['high']) for r in selected),'low':min(float(r['low']) for r in selected),
            'END_OHLC':{k:float(selected[-1][k]) for k in ('open','high','low','close')},
            'OHLC':[{'time':int(r['time']),**{k:float(r[k]) for k in ('open','high','low','close')}} for r in selected],
            'repeated_plot_cells':len(common)*16,'max_recurrence_RMSE':max(f['rmse'] for f in j['Lite_fits'].values())})
    # Single-candle attempt with date explicitly corrected: pair c/d retained.
    a=read(ROOT/'manual'/'Lite_1900_190000_1m_c.csv');b=read(ROOT/'manual'/'Lite_1900_190000_1m_d.csv');ad={int(r['time']):r for r in a}
    assert all(r[k]==ad[int(r['time'])][k] for r in b if int(r['time']) in ad for k in LANES+LAYERS)
    assert any(int(r['time'])==stamp('19:00:00') for r in b)
    assert all(not r[k] for r in b for k in LANES+LAYERS)
    out={'date':'2026-10-12','dt':60,'single_candle':'no observable curves; not C=0',
         'cases':results,'scope':'One episode. Unsampled intermediate END8-10 and12-14 do not establish globally earliest nonfloor window. Local measured transition END19:17 to19:18. C is not restricted to integers.'}
    (ROOT/'C_ventanas_minimas.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ('START','END','bars','Lite_C','compatible_integer_C','high','low')} for r in results],indent=2))
if __name__=='__main__':main()
