"""Control de cobertura identica con distintas agregaciones fuente."""
import csv,json
from pathlib import Path
from datetime import datetime,timezone
from obtener_C import recover
ROOT=Path(__file__).parent
def stamp(s):return int(datetime.fromisoformat('2026-10-12T'+s+'+00:00').timestamp())
def segment(name,start,stop):
    with (ROOT/name).open(encoding='utf-8-sig',newline='') as f:
        return [{**{'time':int(r['time'])},**{k:float(r[k]) for k in ('open','high','low','close')}}
            for r in csv.DictReader(f) if start<=int(r['time'])<stop]
def aggregate(rows,dt):
    groups={}
    for r in rows:groups.setdefault(r['time']//dt*dt,[]).append(r)
    return [{'time':t,'open':g[0]['open'],'high':max(r['high'] for r in g),
        'low':min(r['low'] for r in g),'close':g[-1]['close']} for t,g in sorted(groups.items())]
def analyze_range(start_time,prefix):
    start=stamp(start_time);stop=stamp('19:22:00')
    out=[];fine=None
    for dt,label in ((30,'30s'),(60,'1m'),(120,'2m')):
        name=f'C_agregacion_{prefix}_192130_{label}.csv'
        rows=segment(name,start,stop)
        assert len(rows)==(stop-start)//dt
        assert [r['time'] for r in rows]==list(range(start,stop,dt))
        if fine is None:fine=rows
        assert rows==aggregate(fine,dt),'OHLC fuente difiere de la agregacion de 30s'
        extraction=recover(ROOT/name)
        assert extraction['source_seconds']==dt
        out.append({'source_seconds':dt,'bars':len(rows),'first_source_open':datetime.fromtimestamp(rows[0]['time'],timezone.utc).isoformat(),
            'last_source_open':datetime.fromtimestamp(rows[-1]['time'],timezone.utc).isoformat(),
            'coverage_seconds':stop-start,'range_high':max(r['high'] for r in rows),'range_low':min(r['low'] for r in rows),
            'end_OHLC':{k:rows[-1][k] for k in ('open','high','low','close')},'extraction':extraction})
    assert len({c['range_high'] for c in out})==1 and len({c['range_low'] for c in out})==1
    return {'requested_START_UTC':start_time,'requested_END_UTC':'19:21:30',
        'actual_source_coverage_UTC':f'[{start_time},19:22:00)','OHLC_aggregation_exact':True,'cases':out}
def main():
    result={'ranges':[analyze_range('18:54:00','1854'),analyze_range('18:00:00','1800')]}
    (ROOT/'C_agregacion.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps([{'START':r['requested_START_UTC'],'cases':[{k:c[k] for k in ('source_seconds','bars','end_OHLC')}|
        {'C':c['extraction']['compatible_integer_C_seconds'],'C_interval':c['extraction']['C_seconds_interval']} for c in r['cases']]} for r in result['ranges']],indent=2))
if __name__=='__main__':main()
