import csv,json
from pathlib import Path
from datetime import datetime,timezone
import identificar_emas as model
ROOT=Path(__file__).parent
CASES=[('character_manual_15m_1m.csv','04:45','05:00'),
       ('character_manual_30m_1m_recarga.csv','04:45','05:15'),
       ('character_5m.csv','04:45','04:50'),
       ('character_20m.csv','04:45','05:05'),
       ('character_40m.csv','04:45','05:25'),
       ('character_recent_20m.csv','19:00','19:20'),
       ('character_recent_30m.csv','18:50','19:20'),
       ('character_recent_bear_end_break.csv','19:11','19:31'),
       ('character_recent_15s.csv','19:11','19:31',15),
       ('character_short_15s.csv','19:18','19:20',15)]
def stamp(s):
    return int(datetime.fromisoformat('2026-10-12T'+s+':00+00:00').timestamp())
out=[]
for case in CASES:
    fn,start,end=case[:3]
    step=case[3] if len(case)>3 else 60
    path=ROOT/fn
    result=model.analyze(path,step)
    rows=list(csv.DictReader(path.open(encoding='utf-8-sig')))[:-1]
    result['start']=start;result['end']=end
    result['duration_minutes']=(stamp(end)-stamp(start))/60
    ends=[r for r in rows if int(r['time'])==stamp(end)]
    result['anchor_ohlc']={k:float(ends[0][k])for k in ['open','high','low','close']} if ends else None
    for col,l in result['layers'].items():
        first=next(r for r in rows if r[col])
        future=[r for r in rows if stamp(end)<int(r['time'])<=int(first['time'])]
        # Reverse updates to recover the state at the selected END candle.
        if ends:
            value=float(first[col]); a=l['alpha']
            for r in reversed(future):
                value=(value-a*float(r['close']))/(1-a)
            l['seed_at_end_if_all_closes_processed']=value
        l.pop('alternatives')
    out.append(result)
(ROOT/'estudio_rangos.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
for r in out:
    print(r['file'].split('\\')[-1],r['start'],r['end'],[(k,round(v['period'],6))for k,v in r['layers'].items()])
    print('anchor',r['anchor_ohlc'],'seeds',[(k,round(v.get('seed_at_end_if_all_closes_processed',0),5))for k,v in r['layers'].items()])
