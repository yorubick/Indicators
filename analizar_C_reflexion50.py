"""Auditoría preregistrada de 70000-P: acepta cualquier C coherente entre canales."""
import hashlib
import json
from pathlib import Path
from analizar_C_escala50 import measurement, START, END
from analizar_C_frontera_1s import read
from analizar_C_fuente_vs_grafico import LANES
from analizar_C_traslacion50 import comparison
from auditar_C_escala_50_completa import reconstruct

ROOT=Path(__file__).parent

def reflection(a,b):
    ts=sorted(set(a)&set(b))
    assert ts
    mapping={'open':'open','close':'close','high':'low','low':'high'}
    errors={k:max(abs(float(b[t][k])+float(a[t][v])-70000) for t in ts) for k,v in mapping.items()}
    volume=sum(a[t]['Volume']!=b[t]['Volume'] for t in ts)
    assert max(errors.values())==0 and volume==0
    lanes={}
    for k in LANES:
        es=[abs(float(b[t][k])+float(a[t][k])-70000) for t in ts if a[t][k] and b[t][k]]
        lanes[k]={'max_error':max(es,default=None),'visibility_mismatches':sum(bool(a[t][k])!=bool(b[t][k]) for t in ts)}
    assert max(errors.values()) == 0 and volume == 0
    assert all(v['max_error'] is None or v['max_error'] < 1e-8 for v in lanes.values())
    assert all(v['visibility_mismatches'] == 0 for v in lanes.values())
    return {'common_closed_bars':len(ts),'OHLC_max_errors':errors,'volume_mismatches':volume,'same_lane_reflection':lanes,'tolerance':1e-8}

def rupture(rows):
    high=max(float(rows[t]['high']) for t in range(START,END+1,60))
    low=min(float(rows[t]['low']) for t in range(START,END+1,60))
    t=next(t for t in range(END+60,END+3660,60) if float(rows[t]['close'])>high or float(rows[t]['close'])<low)
    bull=float(rows[t]['close'])>high
    return {'time':t,'direction':'bull' if bull else 'bear','END_seed':float(rows[END]['low' if bull else 'high']),
            'first_visible_by_lane':{k:min(s for s,r in rows.items() if s>END and r[k]) for k in LANES}}

def main():
    names=['base','reflejo_a','reflejo_b','regreso']
    paths={n:ROOT/'manual'/f'C_reflexion50_{n}.csv' for n in names}
    rows={n:read(p) for n,p in paths.items()}
    measurements={n:measurement(r) for n,r in rows.items()}
    recurrence={n:reconstruct(rows[n],START,END,60,measurements[n]['C']) for n in names}
    assert all(v['max_reconstruction_error']<1e-8 and v['visibility_mismatches']==0 for v in recurrence.values())
    result={'preregistered':'C_REFLEXION_50_PREREGISTRO.json','measurements':measurements,'recurrence_540_post_END':recurrence,
            'checks':{'reflection':reflection(rows['base'],rows['reflejo_b']),
                      'repeat':comparison(rows['reflejo_a'],rows['reflejo_b']),
                      'return':comparison(rows['base'],rows['regreso'])},
            'rupture':{n:rupture(rows[n]) for n in ['base','reflejo_b']},
            'sha256':{n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in paths.items()},
            'interpretation':'Observed C=50 in original, reflected price and return. Same lanes reflect within numerical precision. Single window; this does not establish harmonics, a universal symmetry or independence from hidden context.'}
    (ROOT/'C_reflexion50_resultados.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'C':{n:v['C'] for n,v in result['measurements'].items()},'checks':result['checks'],'rupture':result['rupture']},indent=2))

if __name__=='__main__':main()
