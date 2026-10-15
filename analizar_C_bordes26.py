"""Audita cruce de bordes con conteo fijo y controles de END."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from analizar_C_frontera_1s import read
from analizar_C_fuente_vs_grafico import fit_lite, LANES
from analizar_C_traslacion50 import comparison

ROOT=Path(__file__).parent
SPEC=json.loads((ROOT/'C_BORDES_26_PREREGISTRO.json').read_text())

def stamp(time):
    return int(datetime.fromisoformat('2026-10-12T'+time+':00+00:00').timestamp())

def main():
    baseline=read(ROOT/'manual/C_simetria1855_base.csv')
    results=[]
    hashes={}
    for case in SPEC['cases']:
        s,e=stamp(case['START']),stamp(case['END'])
        paths=[ROOT/'manual'/f'C_startSweep1920_bordes_{case["id"]}_{suffix}.csv' for suffix in ['a','b']]
        a,b=[read(p) for p in paths]
        repeat=comparison(a,b)
        common=set(baseline)&set(b)
        assert all(baseline[t][k]==b[t][k] for t in common for k in ['open','high','low','close','Volume'])
        window=list(range(s,e+1,60))
        assert len(window)==case['n'] and all(t in b for t in window)
        assert all(t in b for t in range(e+60,e+3660,60))
        fits=fit_lite(b,60,60)
        cs=[v['C'] for v in fits.values()]
        assert max(cs)-min(cs)<1e-6 and max(v['rmse'] for v in fits.values())<1e-8
        hi=max(float(b[t]['high']) for t in window)
        lo=min(float(b[t]['low']) for t in window)
        rupture=next(t for t in range(e+60,e+3660,60) if float(b[t]['close'])>hi or float(b[t]['close'])<lo)
        bull=float(b[rupture]['close'])>hi
        assert all(min(t for t,r in b.items() if t>e and r[k])==rupture for k in LANES)
        results.append({**case,'C':sum(cs)/6,'H':hi,'L':lo,'range':hi-lo,
                        'rupture_UTC':datetime.fromtimestamp(rupture,timezone.utc).isoformat(),
                        'END_to_rupture_seconds':rupture-e,'direction':'bull' if bull else 'bear',
                        'seed':float(b[e]['low' if bull else 'high']),
                        'START_OHLC':{k:float(b[s][k]) for k in ['open','high','low','close']},
                        'END_OHLC':{k:float(b[e][k]) for k in ['open','high','low','close']},
                        'high_times':[datetime.fromtimestamp(t,timezone.utc).strftime('%H:%M') for t in window if float(b[t]['high'])==hi],
                        'low_times':[datetime.fromtimestamp(t,timezone.utc).strftime('%H:%M') for t in window if float(b[t]['low'])==lo],
                        'repeat_common_bars':repeat['common_closed_bars'],'native_common_bars':len(common),'fits':fits})
        hashes.update({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    path=ROOT/'manual/C_startSweep1920_bordes_regreso.csv'
    returned=read(path)
    check=comparison(baseline,returned)
    hashes[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    return_fits=fit_lite(returned,60,60)
    assert all(abs(v['C']-62)<1e-6 for v in return_fits.values())
    out={'preregistered':SPEC,'results':results,'return_check':check,'return_fits':return_fits,'sha256':hashes,
         'interpretation':'The three 26-bar windows have C134,62,134. Count-only is rejected locally. Window geometry, absolute times, post-END delay and seed are documented confounds; no hidden anchor is identified.'}
    (ROOT/'C_bordes26_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'table':[{k:r[k] for k in ['START','END','n','C','H','L','rupture_UTC','seed','END_to_rupture_seconds','START_OHLC','END_OHLC']} for r in results],'return_verified':True},indent=2))

if __name__=='__main__':main()
