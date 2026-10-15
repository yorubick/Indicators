"""Audita nuevas mediciones solicitadas: serieEND17 y fuentes15/60/120."""
import json,math
from datetime import datetime,timezone
from analizar_C_fuente_vs_grafico import ROOT,read,fit_lite,COLS
from obtener_C import recover
from probar_C_contacto_ruptura21 import FACTORS

def stamp(t):return int(datetime.fromisoformat('2026-10-12T'+t+'+00:00').timestamp())
def iso(t):return datetime.fromtimestamp(t,timezone.utc).isoformat()

def audit(prefix,start,end,dt,both=False):
    pair=next(([x,y] for x,y in [('g','h'),('e','f'),('c','d')] if (ROOT/'manual'/f'{prefix}_{y}.csv').exists()),['a','b'])
    a,b=[read(f'{prefix}_{s}.csv') for s in pair];common=set(a)&set(b);assert common
    columns=COLS if both else list(FACTORS)
    assert all(a[t][k]==b[t][k] for t in common for k in columns),'curves unstable '+prefix
    selected=[{'time':t,**{k:float(b[t][k]) for k in ['open','high','low','close']},'volume':float(b[t]['Volume'])} for t in range(start,end+1,dt)]
    assert all(a[r['time']]['Volume']==b[r['time']]['Volume'] and all(a[r['time']][k]==b[r['time']][k] for k in ['open','high','low','close']) for r in selected)
    fits=fit_lite(b,dt,dt);Cs=[x['C'] for x in fits.values()];C=sum(Cs)/6
    assert max(Cs)-min(Cs)<1e-7 and max(x['rmse'] for x in fits.values())<1e-8
    # Check configured endpoint and gate using first published samples.
    H=max(r['high'] for r in selected);L=min(r['low'] for r in selected)
    post=sorted(t for t in b if t>end);bt=next(t for t in post if float(b[t]['close'])>H or float(b[t]['close'])<L)
    assert min(t for t in b if any(b[t][k] for k in FACTORS))==bt
    seed=selected[-1]['low'] if float(b[bt]['close'])>H else selected[-1]['high'];errors=[]
    for k,factor in FACTORS.items():
        alpha=2/(factor*C/dt+1);v=seed
        for t in range(end+dt,bt+1,dt):v+=alpha*(float(b[t]['close'])-v)
        errors.append(abs(v-float(b[bt][k])))
    assert max(errors)<1e-7,(prefix,'wrong endpoint/seed',errors)
    iv=None
    if both:
        iv=recover(ROOT/'manual'/f'{prefix}_{pair[1]}.csv')['C_seconds_interval']
        assert iv['lower_inclusive']-1e-8<=C<iv['upper_exclusive']+1e-8,(prefix,'Character mismatch',C,iv)
    return {'id':prefix,'START':iso(start),'END':iso(end),'dt':dt,'chart_seconds':dt,'bars':len(selected),'C':C,'C_Lite':C,
            'C_Character_interval':iv,'verification':'sixLite recurrence+repeat+exactOHLCV+ENDseed/firstgate'+('+Character agreement' if both else '; Character anchors not swept'),
            'pair':pair,'OHLC':[{k:v for k,v in r.items() if k!='volume'} for r in selected],'OHLCV':selected,
            'high':H,'low':L,'first_break_after_END':bt,'Lite_fits':fits,'repeat_curve_cells':len(common)*len(columns),'first_sample_seed_max_error':max(errors),
            'source_files':[str(ROOT/'manual'/f'{prefix}_{s}.csv') for s in pair]}

def main():
    start=stamp('18:55:00');cases=[]
    for end in range(stamp('19:20:00'),stamp('19:24:00')+1,15):
        tag=datetime.fromtimestamp(end,timezone.utc).strftime('%H%M%S');cases.append(audit('C_pack_END'+tag,start,end,15))
    for a,b in zip(cases,cases[1:]):assert a['OHLCV']==b['OHLCV'][:-1]
    sweep={'date':'2026-10-12','timezone':'UTC','source_and_chart_seconds':15,'START':iso(start),'END_inclusive_sequence':'19:20:00..19:24:00 step15s:17positions,16increments',
           'scope':'NativeLite only sweep; Character kept at19:20 and is not used for perstep C. No prediction fitted. Two exports and anchor screenshot per subminute position.',
           'cases':cases}
    (ROOT/'C_barrido_END_1855_1920_1924_15s.json').write_text(json.dumps(sweep,indent=2),encoding='utf-8')
    tf=[audit(f'C_pack_tf{dt}',stamp('19:00:00'),stamp('19:20:00'),dt,True) for dt in [15,60,120]]
    out={'date':'2026-10-12','START':'19:00:00 UTC','END':'19:20:00 UTC',
         'interpretation':'Same anchor opening timestamps, different n and OHLCaggregation. Included ENDcandles end at20:15/21:00/22:00 respectively(exclusive). Not isolated charttimeframe invariance with fixed source or identical input trajectory. 2m has n11, short branch.',
         'cases':tf}
    (ROOT/'C_test_timeframes_1900_1920.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'sweep':[(c['END'][11:19],round(c['C'],8)) for c in cases],'timeframes':[(c['dt'],c['bars'],c['C']) for c in tf]},indent=2))

if __name__=='__main__':main()
