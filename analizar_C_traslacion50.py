"""Audita P+10000 contra referencia fresca y regreso; última fila excluida."""
import hashlib
import json
from pathlib import Path
from analizar_C_escala50 import measurement, START, END
from analizar_C_frontera_1s import read
from analizar_C_fuente_vs_grafico import LANES
from auditar_C_escala_50_completa import reconstruct

ROOT = Path(__file__).parent

def comparison(a,b,offset=0):
    common = sorted(set(a)&set(b))
    assert common
    result = {}
    for col in ['open','high','low','close','Volume']+LANES:
        delta = offset if col!='Volume' else 0
        errors = [abs(float(b[t][col])-float(a[t][col])-delta) for t in common if a[t][col] and b[t][col]]
        missing = sum(bool(a[t][col])!=bool(b[t][col]) for t in common)
        tolerance = 1e-8 if col in LANES else 0
        assert missing==0
        assert max(errors,default=0)<=tolerance
        result[col] = {'max_error':max(errors,default=None),'visibility_mismatches':missing,'tolerance':tolerance}
    return {'common_closed_bars':len(common),'columns':result}

def main():
    names = ['base','mas10000_a','mas10000_b','regreso']
    paths = {n:ROOT/'manual'/f'C_traslacion50_{n}.csv' for n in names}
    rows = {n:read(p) for n,p in paths.items()}
    result = {
      'preregistered':'C_TRASLACION_50_PREREGISTRO.json',
      'range':'12 October 2026 19:02–19:22 UTC, 21 bars; chart/source 60s',
      'expression_retained_in_UI':'CME_MINI:NQ1!+10000',
      'measurements':{n:measurement(r) for n,r in rows.items()},
      'recurrence_540_post_END':{n:reconstruct(rows[n],START,END,60,measurement(rows[n])['C']) for n in rows},
      'comparisons':{
        'translation':comparison(rows['base'],rows['mas10000_b'],10000),
        'repeat':comparison(rows['mas10000_a'],rows['mas10000_b']),
        'return':comparison(rows['base'],rows['regreso']),
        'prior_native_baseline':comparison(read(ROOT/'manual'/'C_escala50_base_b.csv'),rows['base'])},
      'sha256':{n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in paths.items()},
      'result':'C=50 before, after P+10000, and on return. Translation matches OHLCV exactly and Lite curves within floating-point precision.',
      'limits':'Single window. Both Gemini v4 and translation invariance predict 50. Does not establish harmonics or exclude indirect level dependence in other regimes. Synthetic metadata/internal requests not fully observable.'}
    assert all(abs(v['C']-50)<1e-6 for v in result['measurements'].values())
    assert all(v['max_reconstruction_error']<1e-8 and v['visibility_mismatches']==0
               for v in result['recurrence_540_post_END'].values())
    (ROOT/'C_traslacion50_resultados.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'C':{n:v['C'] for n,v in result['measurements'].items()},'comparison_bars':{n:v['common_closed_bars'] for n,v in result['comparisons'].items()},'all_checks_passed':True},indent=2))

if __name__=='__main__':main()
