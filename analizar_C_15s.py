"""Construye el registro de sensibilidad de START en velas de 15 segundos."""
import csv, json
from datetime import datetime, timezone
from pathlib import Path
from obtener_C import recover
ROOT = Path(__file__).parent

def stamp(t):
    return int(datetime.fromisoformat('2026-10-12T'+t+'+00:00').timestamp())

def main():
    results=[]
    for path in sorted(ROOT.glob('C_15s_start*.csv')):
        token=path.stem.removeprefix('C_15s_start')
        if len(token)!=6 or not token.isdigit():continue
        start=':'.join([token[:2],token[2:4],token[4:]])
        rows=list(csv.DictReader(path.open(encoding='utf-8-sig')))
        seg=[r for r in rows if stamp(start)<=int(r['time'])<=stamp('19:20:00')]
        assert int(seg[0]['time'])==stamp(start)
        assert int(seg[-1]['time'])==stamp('19:20:00')
        extracted=recover(path)
        record={'START_UTC':start,'END_UTC':'19:20:00','range_high':max(float(r['high'])for r in seg),
                'range_low':min(float(r['low'])for r in seg),'bars':len(seg),
                'start_OHLC':{k:float(seg[0][k])for k in ['open','high','low','close']},
                'end_OHLC':{k:float(seg[-1][k])for k in ['open','high','low','close']},
                'extraction':extracted}
        results.append(record)
        print(start,extracted['compatible_integer_C_seconds'],record['range_high'],record['range_low'])
    assert len(results)==13
    assert len({(r['range_high'],r['range_low'])for r in results})==1
    assert len({tuple(r['end_OHLC'].values())for r in results})==1
    common_reference=None
    for case in results:
        path=Path(case['extraction']['file'])
        common=[(int(r['time']),*(float(r[k])for k in ['open','high','low','close']))
                for r in csv.DictReader(path.open(encoding='utf-8-sig'))
                if stamp('18:57:00')<=int(r['time'])<=stamp('19:20:00')]
        if common_reference is None:common_reference=common
        assert common==common_reference
    reference=recover(ROOT/'C_15s_start1855_reference.csv')
    repeated=recover(ROOT/'C_15s_start185430_repeat.csv')
    for case in results:
        if case['START_UTC']=='18:55:00':assert case['extraction']['periods']==reference['periods']
        if case['START_UTC']=='18:54:30':assert case['extraction']['periods']==repeated['periods']
    output={'date_UTC':'2026-10-12','profile':'B','source_seconds':15,'cases':results,
            'reference_185500':reference,'repeated_185430':repeated,
            'scope':'C extraido de los plots originales; formula generadora pendiente.'}
    ends=[]
    for end in ['19:18:00','19:19:00','19:20:00','19:21:00','19:22:00']:
        path=ROOT/('C_15s_start185500.csv' if end=='19:20:00' else
                   'C_15s_start185500_end'+end.replace(':','')+'.csv')
        rows=list(csv.DictReader(path.open(encoding='utf-8-sig')))
        seg=[r for r in rows if stamp('18:55:00')<=int(r['time'])<=stamp(end)]
        assert int(seg[-1]['time'])==stamp(end)
        record={'START_UTC':'18:55:00','END_UTC':end,'extraction':recover(path),
                'range_high':max(float(r['high'])for r in seg),
                'range_low':min(float(r['low'])for r in seg),
                'end_OHLC':{k:float(seg[-1][k])for k in ['open','high','low','close']}}
        ends.append(record)
        print('END',end,record['extraction']['compatible_integer_C_seconds'])
    output['END_controls']=ends
    output['matched_coverage_control']={'START_UTC':'18:55:00','END_UTC':'19:20:45',
        'extraction':recover(ROOT/'C_15s_start185500_end192045.csv'),
        'one_minute_reference':recover(ROOT/'C_25m_live_confirmado.csv'),
        'scope':'Misma cobertura temporal hasta 19:20:59, distinta agregacion y OHLC de END.'}
    fine=list(csv.DictReader((ROOT/'C_15s_start185500_end192045.csv').open(encoding='utf-8-sig')))
    coarse=list(csv.DictReader((ROOT/'C_25m_live_confirmado.csv').open(encoding='utf-8-sig')))
    coarse={int(r['time']):r for r in coarse}
    groups={}
    for r in fine:
        t=int(r['time'])
        if stamp('18:55:00')<=t<=stamp('19:20:45'):groups.setdefault(t//60*60,[]).append(r)
    assert len(groups)==26
    for t,bars in groups.items():
        assert len(bars)==4
        aggregated={'open':float(bars[0]['open']),'high':max(float(r['high'])for r in bars),
                    'low':min(float(r['low'])for r in bars),'close':float(bars[-1]['close'])}
        assert aggregated=={k:float(coarse[t][k])for k in aggregated},t
    output['matched_coverage_control']['aggregated_15s_matches_1m_OHLC_bars']=26
    output['common_START_sweep_OHLC_identical']=True
    (ROOT/'C_sensibilidad_15s.json').write_text(json.dumps(output,indent=2),encoding='utf-8')

if __name__=='__main__':main()
