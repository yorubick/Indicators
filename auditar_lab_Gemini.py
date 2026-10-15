"""Emula la recurrencia del Pine recibido; no compila ni ejecuta Pine."""
import csv,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).parent
LANES=['Lane 3 A','Lane 3 B','Lane 2 A','Lane 2 B','Lane 1 A','Lane 1 B']
BASES=[72/3,89/3,72/9,89/9,72/27,89/27]
def stamp(t):return int(datetime.fromisoformat(t.replace('Z','+00:00')).timestamp())
def main():
    cases=[]
    for name in ['Lite_1855_1920_1m_comparacion.json','Lite_185415_1920_15s_comparacion.json','Lite_0445_053000_1m_comparacion.json']:
        info=json.loads((ROOT/name).read_text(encoding='utf-8-sig'))
        with Path(info['file']).open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))[:-1]
        start,end=stamp(info['START_UTC']),stamp(info['END_UTC']);dt=info['chart_seconds']
        C=info['Character_extraction']['compatible_integer_C_seconds'][0]
        endpoint=next(r for r in rows if int(r['time'])==end)
        post=[r for r in rows if end<int(r['time'])<=end+5400]
        assert [int(r['time']) for r in post]==list(range(end+dt,end+5401,dt))
        periods=[base*C/dt for base in BASES];state=None;errors=[];first_errors={};premature=0
        for r in post:
            # Pine lines100-103: first active bar returns seed without close update.
            if state is None:state=[float(endpoint['low'])]*6
            else:state=[y+2/(N+1)*(float(r['close'])-y) for y,N in zip(state,periods)]
            for lane,y in zip(LANES,state):
                if r[lane]:
                    error=abs(float(r[lane])-y);errors.append(error)
                    first_errors.setdefault(lane,{'UTC':datetime.fromtimestamp(int(r['time']),timezone.utc).isoformat(),'error_points':error})
                else:premature+=1
        cases.append({'comparison':name,'C_supplied_correctly':C,'chart_seconds_matches_res_sec':dt,
                      'first_visible_errors':first_errors,'maximum_visible_error_points':max(errors),
                      'premature_plot_cells':premature,'compared_values':len(errors)})
    out={'scope':'Offline numerical emulation of supplied Pine manual EMA state, using correct C, matching resolution and exact END. No Pine compiler validation. Original Gemini file unchanged.', 'cases':cases}
    (ROOT/'Gemini_lab_auditoria.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
