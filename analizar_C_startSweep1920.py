"""Audita barrido preregistrado START móvil / END fijo, sin ajustar modelo."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from analizar_C_frontera_1s import read
from analizar_C_fuente_vs_grafico import fit_lite, LANES
from analizar_C_traslacion50 import comparison

ROOT=Path(__file__).parent
SPEC=json.loads((ROOT/'C_START_SWEEP_1920_PREREGISTRO.json').read_text())
END=int(datetime.fromisoformat(SPEC['END_UTC'].replace('Z','+00:00')).timestamp())

def main():
    baseline=read(ROOT/'manual/C_simetria1855_base.csv')
    results=[]
    hashes={}
    for time in SPEC['START_times_UTC']:
        start=int(datetime.fromisoformat('2026-10-12T'+time+':00+00:00').timestamp())
        paths=[ROOT/'manual'/f'C_startSweep1920_{time.replace(":","")}_{suffix}.csv' for suffix in ['a','b']]
        a,b=[read(p) for p in paths]
        repeated=comparison(a,b)
        common=sorted(set(baseline)&set(b))
        assert all(baseline[t][k]==b[t][k] for t in common for k in ['open','high','low','close','Volume'])
        stamps=list(range(start,END+1,60))
        assert all(t in b for t in stamps)
        assert all(t in b for t in range(END+60,END+3660,60))
        fits=fit_lite(b,60,60)
        cs=[v['C'] for v in fits.values()]
        assert max(cs)-min(cs)<1e-6 and max(v['rmse'] for v in fits.values())<1e-8
        hi=max(float(b[t]['high']) for t in stamps)
        lo=min(float(b[t]['low']) for t in stamps)
        rupture=next(t for t in range(END+60,END+3660,60) if float(b[t]['close'])>hi or float(b[t]['close'])<lo)
        bull=float(b[rupture]['close'])>hi
        first={k:min(t for t,r in b.items() if t>END and r[k]) for k in LANES}
        assert all(t==rupture for t in first.values())
        result={'START':time,'n':len(stamps),'C':sum(cs)/6,'H':hi,'L':lo,'range':hi-lo,
                'rupture_UTC':datetime.fromtimestamp(rupture,timezone.utc).isoformat(),'direction':'bull' if bull else 'bear',
                'seed':float(b[END]['low' if bull else 'high']),
                'start_open':float(b[start]['open']),'start_close':float(b[start]['close']),
                'END_close':float(b[END]['close']),
                'high_times':[datetime.fromtimestamp(t,timezone.utc).strftime('%H:%M') for t in stamps if float(b[t]['high'])==hi],
                'low_times':[datetime.fromtimestamp(t,timezone.utc).strftime('%H:%M') for t in stamps if float(b[t]['low'])==lo],
                'repeat_common_bars':repeated['common_closed_bars'],'native_common_bars':len(common),'fits':fits}
        results.append(result)
        hashes.update({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    reference=next(r for r in results if r['START']=='18:55')
    same=[r['START'] for r in results if all(r[k]==reference[k] for k in ['H','L','rupture_UTC','direction','seed'])]
    path=ROOT/'manual/C_startSweep1920_regreso.csv'
    returned=read(path)
    check=comparison(read(ROOT/'manual/C_startSweep1920_1855_b.csv'),returned)
    comparison(baseline,returned)
    hashes[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    return_fits=fit_lite(returned,60,60)
    assert all(abs(v['C']-62)<1e-6 for v in return_fits.values())
    out={'preregistered':SPEC,'results':results,'same_extrema_rupture_seed_as_1855':same,
         'return_check':check,'return_fits':return_fits,'sha256':hashes,
         'limits':'START count and included geometry vary together; equal extrema and rupture do not fix all normalized shape/history. All inferred rules after sweep are exploratory.'}
    (ROOT/'C_startSweep1920_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'table':[{k:r[k] for k in ['START','n','C','H','L','rupture_UTC','seed']} for r in results],'same_controls_as1855':same},indent=2))

if __name__=='__main__':main()
