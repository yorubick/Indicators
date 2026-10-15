import csv,json,math
from pathlib import Path
from datetime import datetime
from comparar_Lite_Character import LANES
ROOT=Path(__file__).parent
LAYERS=['Layer A','Layer A boundary','Layer B','Layer B boundary','Layer C','Layer C boundary','Extra cloud 1','Extra cloud 1 boundary','Extra cloud 2','Extra cloud 2 boundary']
def read(p):
    with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))[:-1]
def main():
    cases=[]
    for p in sorted(ROOT.glob('Lite_*_comparacion.json')):
        j=json.loads(p.read_text(encoding='utf-8-sig'));s,e=j['START_UTC'],j['END_UTC']
        if s[:10]!='2026-10-12' or j['chart_seconds']!=60 or not '19:00:00'<=s[11:19]<='19:04:00' or not '19:20:00'<=e[11:19]<='19:30:00':continue
        bpath=Path(j['file']);suffix=bpath.stem[-1];apath=bpath.with_name(bpath.name[:-5]+('a' if suffix=='b' else 'c')+'.csv')
        a,b=read(apath),read(bpath);ad={int(r['time']):r for r in a};common=[r for r in b if int(r['time']) in ad]
        assert common and all(r[k]==ad[int(r['time'])][k] for r in common for k in LANES+LAYERS),p
        lo,hi=[int(datetime.fromisoformat(t.replace('Z','+00:00')).timestamp()) for t in (s,e)]
        selected=[r for r in b if lo<=int(r['time'])<=hi]
        assert [int(r['time']) for r in selected]==list(range(lo,hi+1,60)),p
        cs=list(j['Lite_C_assuming_unrounded_family'].values());C=sum(cs)/6;it=j['Character_extraction']['C_seconds_interval']
        assert max(cs)-min(cs)<1e-8 and it['lower_inclusive']-1e-8<=C<it['upper_exclusive']+1e-8,p
        cases.append({'START':s[11:19],'END':e[11:19],'bars':len(selected),'C':C,
          'high':max(float(r['high']) for r in selected),'low':min(float(r['low']) for r in selected),
          'first_OHLC':{k:float(selected[0][k]) for k in ('open','high','low','close')},
          'last_OHLC':{k:float(selected[-1][k]) for k in ('open','high','low','close')},
          'file':str(bpath),'OHLC':selected})
        row=cases[-1]
        breakout=next((r for r in b if int(r['time'])>hi and (float(r['close'])>row['high'] or float(r['close'])<row['low'])),None)
        row['first_breakout']=None if breakout is None else {
          'UTC':datetime.fromtimestamp(int(breakout['time']),datetime.fromisoformat(s.replace('Z','+00:00')).tzinfo).isoformat(),
          'bars_after_END':(int(breakout['time'])-hi)//60,'close':float(breakout['close']),
          'direction':'bull' if float(breakout['close'])>row['high'] else 'bear'}
    predictions=[{'START':'19:03:00','END':'19:24:00','predicted_C':52}, {'START':'19:02:00','END':'19:25:00','predicted_C':57}]
    for p in predictions:
        r=next(r for r in cases if r['START']==p['START'] and r['END']==p['END']);p.update(measured_C=r['C'],match=abs(r['C']-p['predicted_C'])<1e-7)
    out={'cases':cases,'predeclared_count_predictions':predictions,'scope':'Incomplete triangular matrix, one day; cannot infer universal selector. No global source floor.'}
    (ROOT/'C_matriz.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in r.items() if k not in ('OHLC','first_OHLC','file')} for r in cases],indent=2))
    print(json.dumps(predictions,indent=2))
if __name__=='__main__':main()
