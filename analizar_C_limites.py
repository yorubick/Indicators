"""Contrastes de limites del rango y del OHLC final. No genera C desde precios."""
import csv,json
from pathlib import Path
from datetime import datetime
from obtener_C import recover
ROOT=Path(__file__).parent
def stamp(t):return int(datetime.fromisoformat('2026-10-12T'+t+'+00:00').timestamp())
cases=[
 ('C_15s_start185500.csv','18:55:00','19:20:00',15),
 ('C_end_quarter_192015.csv','18:55:00','19:20:15',15),
 ('C_end_quarter_192030.csv','18:55:00','19:20:30',15),
 ('C_15s_start185500_end192045.csv','18:55:00','19:20:45',15),
 ('C_1m_start185400_end192000.csv','18:54:00','19:20:00',60),
 ('C_1m_start185415_end192000.csv','18:54:15','19:20:00',60),
 ('C_1m_start185430_end192000.csv','18:54:30','19:20:00',60),
 ('C_25m_live_confirmado.csv','18:55:00','19:20:00',60),
 ('C_1m_start185500_end192030.csv','18:55:00','19:20:30',60)]
out=[]
for name,start,end,dt in cases:
    path=ROOT/name;rows=list(csv.DictReader(path.open(encoding='utf-8-sig')))
    seg=[r for r in rows if stamp(start)<=int(r['time'])<=stamp(end)]
    extracted=recover(path)
    assert extracted['source_seconds']==dt
    record={'requested_START_UTC':start,'requested_END_UTC':end,'source_seconds':dt,
            'first_source_open_UTC':datetime.fromtimestamp(int(seg[0]['time']),__import__('datetime').timezone.utc).strftime('%H:%M:%S'),
            'last_source_open_UTC':datetime.fromtimestamp(int(seg[-1]['time']),__import__('datetime').timezone.utc).strftime('%H:%M:%S'),
            'bars_in_timestamp_window':len(seg),'range_high':max(float(r['high'])for r in seg),
            'range_low':min(float(r['low'])for r in seg),
            'end_OHLC':{k:float(seg[-1][k])for k in ['open','high','low','close']},
            'extraction':extracted}
    out.append(record)
    print(start,end,dt,extracted['compatible_integer_C_seconds'])
assert out[0]['range_high']==out[2]['range_high']
assert out[0]['range_low']==out[2]['range_low']
assert out[0]['end_OHLC']['low']==out[2]['end_OHLC']['low']
assert out[0]['extraction']['periods']!=out[2]['extraction']['periods']
for i in [5,6,8]:assert out[i]['extraction']['periods']==out[7]['extraction']['periods']
(ROOT/'C_limites_y_mecha.json').write_text(json.dumps({'cases':out,
    'scope':'Recuperacion de C y evidencia compatible con seleccionar aperturas START<=time<=END; no lectura de codigo privado.'},indent=2),encoding='utf-8')
