import csv,json
from pathlib import Path
from datetime import datetime
from comparar_Lite_Character import LANES
ROOT=Path(__file__).parent
LAYERS=['Layer A','Layer A boundary','Layer B','Layer B boundary','Layer C','Layer C boundary','Extra cloud 1','Extra cloud 1 boundary','Extra cloud 2','Extra cloud 2 boundary']
def read(p):
    with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))[:-1]
def main():
    prefixes=['Lite_190000_'+e+'_15s' for e in ('190430','190445','190500')]+['Lite_20261013_1900_'+e+'_1m' for e in ('191800','191900','1920')]
    out=[]
    for prefix in prefixes:
        j=json.loads((ROOT/(prefix+'_comparacion.json')).read_text(encoding='utf-8-sig'))
        suffixes=('c','d') if '20261013' in prefix else ('a','b')
        a,b=[read(ROOT/'manual'/(prefix+'_'+s+'.csv')) for s in suffixes];ad={int(r['time']):r for r in a}
        common=[r for r in b if int(r['time']) in ad];bad=[(r['time'],k) for r in common for k in LANES+LAYERS if r[k]!=ad[int(r['time'])][k]]
        lo,hi=[int(datetime.fromisoformat(j[k].replace('Z','+00:00')).timestamp()) for k in ('START_UTC','END_UTC')];dt=j['chart_seconds']
        selected=[r for r in b if lo<=int(r['time'])<=hi]
        assert [int(r['time']) for r in selected]==list(range(lo,hi+1,dt)),prefix
        cs=list(j['Lite_C_assuming_unrounded_family'].values());C=sum(cs)/6
        interval=j['Character_extraction']['C_seconds_interval'];prediction=max(dt,len(selected)*dt*10/183)
        assert not bad and interval['lower_inclusive']<=C<interval['upper_exclusive'],prefix
        out.append({'prefix':prefix,'date':j['START_UTC'][:10],'dt':dt,'bars':len(selected),'C_Lite':C,
          'six_curve_spread':max(cs)-min(cs),'formula_prediction':prediction,'formula_match':abs(C-prediction)<1e-7,
          'closed_pair_mismatches':len(bad),'C_in_Character_interval':interval['lower_inclusive']<=C<interval['upper_exclusive'],
          'Character_interval':interval,'OHLC':selected})
    (ROOT/'C_corto_fuentes.json').write_text(json.dumps({'cases':out,'scope':'Two sources/two dates. Warmup branch interpretation unproven.'},indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in r.items() if k!='OHLC'} for r in out],indent=2))
if __name__=='__main__':main()
