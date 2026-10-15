import csv,json
from pathlib import Path
from datetime import datetime
from comparar_Lite_Character import LANES
ROOT=Path(__file__).parent
LAYERS=['Layer A','Layer A boundary','Layer B','Layer B boundary','Layer C','Layer C boundary','Extra cloud 1','Extra cloud 1 boundary','Extra cloud 2','Extra cloud 2 boundary']
def read(p):
    with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))[:-1]
def main():
    prefixes=['Lite_1900_'+e+'_1m' for e in ('192100','192200','192300','192400')]+['Lite_180000_'+e+'_2m' for e in ('183600','183800','184000')]
    cases=[]
    for prefix in prefixes:
        j=json.loads((ROOT/(prefix+'_comparacion.json')).read_text(encoding='utf-8-sig'))
        suffixes=('c','d') if prefix.startswith('Lite_1900_') else ('a','b')
        a,b=[read(ROOT/'manual'/(prefix+'_'+s+'.csv')) for s in suffixes];ad={int(r['time']):r for r in a}
        common=[r for r in b if int(r['time']) in ad]
        assert common and all(r[k]==ad[int(r['time'])][k] for r in common for k in LANES+LAYERS),prefix
        start,end=[int(datetime.fromisoformat(j[k].replace('Z','+00:00')).timestamp()) for k in ('START_UTC','END_UTC')];dt=j['chart_seconds']
        selected=[r for r in b if start<=int(r['time'])<=end]
        assert [int(r['time']) for r in selected]==list(range(start,end+1,dt))
        Cs=list(j['Lite_C_assuming_unrounded_family'].values());C=sum(Cs)/6;interval=j['Character_extraction']['C_seconds_interval']
        assert max(Cs)-min(Cs)<1e-8 and interval['lower_inclusive']<=C<interval['upper_exclusive'],prefix
        prediction=max(dt,len(selected)*dt*10/183)
        cases.append({'prefix':prefix,'START':j['START_UTC'],'END':j['END_UTC'],'dt':dt,'bars':len(selected),'C':C,
          'short_rule_prediction':prediction,'short_rule_match':abs(C-prediction)<1e-7,
          'high':max(float(r['high']) for r in selected),'low':min(float(r['low']) for r in selected),
          'END_OHLC':{k:float(selected[-1][k]) for k in ('open','high','low','close')},'interval_Character':interval,
          'repeated_curve_cells':len(common)*16,'OHLC':selected})
    out={'cases':cases,'scope':'Measured boundary repeats across15/60/120s and two dates; universal threshold and general C generator unproved.'}
    (ROOT/'C_frontera21.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in r.items() if k not in ('OHLC','repeated_curve_cells')} for r in cases],indent=2))
if __name__=='__main__':main()
