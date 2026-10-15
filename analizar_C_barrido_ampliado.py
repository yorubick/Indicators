"""Barrido Manual con dos exportaciones estables por selección nueva.

Archivos provisionales deliberadamente excluidos: pueden contener plots de la
selección anterior aun cuando su recurrencia EMA sea matemáticamente correcta.
"""
import csv,json
from pathlib import Path
from datetime import datetime
from obtener_C import recover
ROOT=Path(__file__).parent

def timestamp(s):
    return int(datetime.fromisoformat('2026-10-12T'+s+'+00:00').timestamp())

def rows(path):
    return {int(r['time']):r for r in csv.DictReader(path.open(encoding='utf-8-sig'))}

def main():
    old=json.loads((ROOT/'C_sensibilidad_15s.json').read_text())['cases']
    reference=rows(ROOT/'C_barrido_15s_start1854_estabilizado.csv')
    controls=[]
    for s in ('1852','1853','1901','1902'):
        a=ROOT/f'C_barrido_15s_start{s}_estabilizado.csv'
        b=ROOT/f'C_barrido_15s_start{s}_verificado.csv'
        if not a.exists() or not b.exists():continue
        x,y=recover(a),recover(b)
        assert x['periods']==y['periods'],s
        ra,rb=rows(a),rows(b)
        common=sorted(set(ra)&set(rb))[:-2]
        plot_columns=list(x['periods'])
        assert all(ra[t][k]==rb[t][k] for t in common for k in plot_columns),s
        controls.append({'START_UTC':s[:2]+':'+s[2:]+':00','END_UTC':'19:20:00',
                         'extraction':y,'repeat_file':str(a),'exact_repeat_plot_values':len(common)*10})
    combined=[]
    for c in old+controls:
        r=rows(Path(c['extraction']['file']))
        start=timestamp(c['START_UTC']);end=timestamp(c['END_UTC'])
        needed=list(range(start,end+1,15))
        assert all(t in r and t in reference for t in needed),c['START_UTC']
        assert all(r[t][k]==reference[t][k] for t in needed for k in ('open','high','low','close')),c['START_UTC']
        seg=[r[t] for t in needed]
        first={k:float(seg[0][k]) for k in ('open','high','low','close')}
        color='bull' if first['close']>first['open'] else 'bear' if first['close']<first['open'] else 'doji'
        pivots={}
        # Strict left, non-strict right; inspect outside selected range only to
        # classify START as a local pivot, never to claim internal availability.
        for radius in (1,2,3,5):
            neighbors=[reference.get(start+i*15) for i in range(-radius,radius+1)]
            assert all(neighbors)
            highs=[float(q['high']) for q in neighbors];lows=[float(q['low']) for q in neighbors]
            high=first['high']>max(highs[:radius]) and first['high']>=max(highs[radius+1:])
            low=first['low']<min(lows[:radius]) and first['low']<=min(lows[radius+1:])
            pivots[str(radius)]='both' if high and low else 'high' if high else 'low' if low else 'none'
        combined.append({'START_UTC':c['START_UTC'],'C':c['extraction']['compatible_integer_C_seconds'][0],
            'bars':len(seg),'first_OHLC':first,'color':color,'pivots':pivots,
            'range_high':max(float(q['high']) for q in seg),'range_low':min(float(q['low']) for q in seg),
            'file':c['extraction']['file'],'new_verified':c in controls})
    def grouped(key):
        out={}
        for c in combined:out.setdefault(key(c),set()).add(c['C'])
        return {k:sorted(v) for k,v in out.items()}
    tests={'color':grouped(lambda c:c['color'])}
    for radius in (1,2,3,5):
        tests[f'pivot_radius_{radius}']=grouped(lambda c:c['pivots'][str(radius)])
        tests[f'color_and_pivot_{radius}']=grouped(lambda c:c['color']+'/'+c['pivots'][str(radius)])
    control=recover(ROOT/'C_barrido_15s_start1854_estabilizado.csv')
    assert control['compatible_integer_C_seconds']==[123]
    output={'END_UTC':'19:20:00','source_seconds':15,'new_controls':controls,'cases':combined,
            'control_1854_reproduces_C123':True,'all_selected_OHLC_matches_reference':True,
            'simple_categorical_tests':tests,
            'scope':'Same day, overlapping Manual ranges. Repeated plots are compared on closed common rows. Local pivots include neighbors outside START, used only as descriptive labels. No generator identified.',
            'excluded_pattern':'C_barrido CSVs without explicit estabilizado/verificado pair; three failed the EMA check, others can be stale but mathematically valid.'}
    (ROOT/'C_barrido_ampliado.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    print(json.dumps({'new_controls':[(c['START_UTC'],c['extraction']['compatible_integer_C_seconds']) for c in controls],
                      'categorical_tests':tests},indent=2))

if __name__=='__main__':main()
