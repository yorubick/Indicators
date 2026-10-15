import csv,json
from pathlib import Path
from datetime import datetime
from comparar_Lite_Character import LANES
ROOT=Path(__file__).parent
LAYERS=['Layer A','Layer A boundary','Layer B','Layer B boundary','Layer C','Layer C boundary','Extra cloud 1','Extra cloud 1 boundary','Extra cloud 2','Extra cloud 2 boundary']
def read(p):
    with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))[:-1]
def main():
    names=['Lite_1901_192100_1m','Lite_1902_192200_1m','Lite_1903_192300_1m','Lite_1904_192400_1m','Lite_1902_192100_1m','Lite_1901_192200_1m']
    cases=[]
    for prefix in names:
        j=json.loads((ROOT/(prefix+'_comparacion.json')).read_text(encoding='utf-8-sig'))
        a,b=[read(ROOT/'manual'/(prefix+'_'+s+'.csv')) for s in ('a','b')];ad={int(r['time']):r for r in a}
        common=[r for r in b if int(r['time']) in ad];bad=[(r['time'],k) for r in common for k in LANES+LAYERS if r[k]!=ad[int(r['time'])][k]]
        start,end=[int(datetime.fromisoformat(j[k].replace('Z','+00:00')).timestamp()) for k in ('START_UTC','END_UTC')]
        selected=[r for r in b if start<=int(r['time'])<=end]
        assert [int(r['time']) for r in selected]==list(range(start,end+1,60)),prefix
        Cs=list(j['Lite_C_assuming_unrounded_family'].values());C=sum(Cs)/6;interval=j['Character_extraction']['C_seconds_interval']
        compatible=interval['lower_inclusive']-1e-8<=C<interval['upper_exclusive']+1e-8
        assert not bad and max(Cs)-min(Cs)<1e-8 and compatible,prefix
        cases.append({'prefix':prefix,'START':j['START_UTC'],'END':j['END_UTC'],'bars':len(selected),'C':C,
          'closed_pair_mismatches':len(bad),'C_in_Character_interval_with_1e_8_tolerance':compatible,
          'Character_C_interval':interval,
          'six_C_spread':max(Cs)-min(Cs),'high':max(float(r['high']) for r in selected),'low':min(float(r['low']) for r in selected),
          'first_OHLC':{k:float(selected[0][k]) for k in ('open','high','low','close')},
          'last_OHLC':{k:float(selected[-1][k]) for k in ('open','high','low','close')},'OHLC':selected})
    tailcase=cases[1];base=json.loads((ROOT/'Lite_1900_192200_1m_comparacion.json').read_text())
    base_rows={int(r['time']):r for r in read(Path(base['file']))}
    same_tail=all(all(float(r[k])==float(base_rows[int(r['time'])][k]) for k in ('open','high','low','close')) for r in tailcase['OHLC'])
    out={'cases':cases,'shared_tail_comparison':{'base':'19:00–19:22','base_bars':23,'base_C':sum(base['Lite_C_assuming_unrounded_family'].values())/6,
          'tail':'19:02–19:22','tail_bars':21,'tail_C':tailcase['C'],'all_last21_OHLC_identical':same_tail},
          'scope':'One date. C below source rules out global C>=dt. Tail counterexample excludes dependence solely on last21 OHLC, not global state/extrema or count.'}
    (ROOT/'C_ventanas_fijas.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({**out,'cases':[{k:v for k,v in r.items() if k!='OHLC'} for r in cases]},indent=2))
if __name__=='__main__':main()
