"""Comprueba predicciones prefijadas y parejas Lite/Character del tramo corto."""
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
    specs=[('18:59:00','19:18:00'),('18:58:00','19:18:00'),('19:01:00','19:19:00'),('18:59:00','19:19:00'),
           ('04:45:00','05:03:00'),('04:45:00','05:04:00'),('04:45:00','05:05:00')]
    out=[]
    for start,end in specs:
        prefix='Lite_'+start[:5].replace(':','')+'_'+end.replace(':','')+'_1m'
        j=json.loads((ROOT/(prefix+'_comparacion.json')).read_text(encoding='utf-8-sig'))
        suffixes=('c','d') if end=='05:05:00' else ('a','b')
        a,b=[read(ROOT/'manual'/(prefix+'_'+s+'.csv')) for s in suffixes];ad={int(r['time']):r for r in a}
        common=[r for r in b if int(r['time']) in ad]
        assert common and all(r[k]==ad[int(r['time'])][k] for r in common for k in LANES+LAYERS),prefix
        selected=[r for r in b if stamp(start)<=int(r['time'])<=stamp(end)]
        assert [int(r['time']) for r in selected]==list(range(stamp(start),stamp(end)+1,60))
        Cs=list(j['Lite_C_assuming_unrounded_family'].values());C=sum(Cs)/6;interval=j['Character_extraction']['C_seconds_interval']
        assert max(Cs)-min(Cs)<1e-8 and interval['lower_inclusive']<=C<interval['upper_exclusive']
        prediction=max(60,len(selected)*200/61)
        out.append({'START':start,'END':end,'bars':len(selected),'measured_C':C,'count_rule_prediction':prediction,
                    'count_rule_match':abs(C-prediction)<1e-7,'prediction_stage':'predeclared' if end!='05:05:00' else 'boundary_extension_previous_Character_C75_known',
                    'high':max(float(r['high']) for r in selected),'low':min(float(r['low']) for r in selected),
                    'interval_Character':interval,'C_six_curve_spread':max(Cs)-min(Cs),'repeated_curve_cells':len(common)*16,
                    'max_recurrence_RMSE':max(f['rmse'] for f in j['Lite_fits'].values()),
                    'OHLC':[{'time':int(r['time']),**{k:float(r[k]) for k in ('open','high','low','close')}} for r in selected]})
    report={'local_hypothesis':'C=max(60,n*200/61), n inclusive bars, source60s; valid boundary not established universally',
            'cases':out,'predeclared_predictions':6,'predeclared_matches':sum(r['count_rule_match'] for r in out[:6]),
            'scope':'Two episodes on one date. 19/20 bars repeat decimals;21 bars invalidate global count-only formula. Fallback/warmup is an interpretation requiring further tests.'}
    (ROOT/'C_regimen_decimal.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ('START','END','bars','measured_C','count_rule_prediction','count_rule_match','high','low')} for r in out],indent=2))
if __name__=='__main__':main()
