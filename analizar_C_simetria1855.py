"""Audita tres transformaciones en segunda ventana, sin exigir C invariante."""
import hashlib
import json
from datetime import datetime
from pathlib import Path
from analizar_C_frontera_1s import read
from analizar_C_fuente_vs_grafico import fit_lite, LANES
from analizar_C_traslacion50 import comparison

ROOT=Path(__file__).parent
START=int(datetime.fromisoformat('2026-10-12T18:55:00+00:00').timestamp())
END=int(datetime.fromisoformat('2026-10-12T19:20:00+00:00').timestamp())

def measure(rows):
    window=list(range(START,END+1,60))
    assert len(window)==26 and all(t in rows for t in window)
    assert all(t in rows for t in range(END+60,END+3660,60))
    fits=fit_lite(rows,60,60)
    cs=[v['C'] for v in fits.values()]
    assert max(cs)-min(cs)<1e-6
    assert max(v['rmse'] for v in fits.values())<1e-8
    hi=max(float(rows[t]['high']) for t in window)
    lo=min(float(rows[t]['low']) for t in window)
    rupture=next(t for t in range(END+60,END+3660,60) if float(rows[t]['close'])>hi or float(rows[t]['close'])<lo)
    return {'C':sum(cs)/6,'range_bars':26,'H':hi,'L':lo,'six_fits':fits,
            'rupture_time':datetime.fromtimestamp(rupture,datetime.fromisoformat('2000-01-01T00:00:00+00:00').tzinfo).isoformat(),
            'rupture_direction':'bull' if float(rows[rupture]['close'])>hi else 'bear'}

def transform(a,b,factor,offset):
    ts=sorted(set(a)&set(b))
    assert ts
    mp={'open':'open','close':'close','high':'high' if factor>0 else 'low','low':'low' if factor>0 else 'high'}
    errors={k:max(abs(float(b[t][k])-factor*float(a[t][v])-offset) for t in ts) for k,v in mp.items()}
    volume=sum(a[t]['Volume']!=b[t]['Volume'] for t in ts)
    assert max(errors.values())==0 and volume==0
    lanes={k:{'max_error':max((abs(float(b[t][k])-factor*float(a[t][k])-offset) for t in ts if a[t][k] and b[t][k]),default=None),
              'visibility_mismatches':sum(bool(a[t][k])!=bool(b[t][k]) for t in ts)} for k in LANES}
    return {'common_closed_bars':len(ts),'OHLC_max_errors':errors,'volume_mismatches':volume,'lane_affine_comparison':lanes}

def main():
    names=['base','doble_a','doble_b','traslacion_a','traslacion_b','reflejo_a','reflejo_b','regreso']
    paths={n:ROOT/'manual'/f'C_simetria1855_{n}.csv' for n in names}
    rows={n:read(p) for n,p in paths.items()}
    out={'preregistered':'C_SIMETRIA_1855_PREREGISTRO.json','measurements':{n:measure(rows[n]) for n in names},
         'transform_checks':{n:transform(rows['base'],rows[n+'_b'],f,o) for n,f,o in [('doble',2,0),('traslacion',1,10000),('reflejo',-1,70000)]},
         'repeat_checks':{n:comparison(rows[n+'_a'],rows[n+'_b']) for n in ['doble','traslacion','reflejo']},
         'return_check':comparison(rows['base'],rows['regreso']),
         'sha256':{n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in paths.items()},
         'limits':'Second overlapping window of same day/instrument, not independent cross-market replication. Hidden metadata/internal requests not observable. Whole available history transformed. No identification of harmonic or temporal generator.'}
    (ROOT/'C_simetria1855_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'C':{n:v['C'] for n,v in out['measurements'].items()},'transform_checks':out['transform_checks'],'return_bars':out['return_check']['common_closed_bars']},indent=2))

if __name__=='__main__':main()
