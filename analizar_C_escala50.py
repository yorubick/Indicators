"""Audita la prueba de escala del 12 octubre; excluye última vela de cada CSV."""
import hashlib
import json
from datetime import datetime
from pathlib import Path
from analizar_C_frontera_1s import read
from analizar_C_fuente_vs_grafico import fit_lite, LANES

ROOT = Path(__file__).parent
START = int(datetime.fromisoformat('2026-10-12T19:02:00+00:00').timestamp())
END = START + 20*60
COLS = ['open','high','low','close','Volume'] + LANES

def load(name):
    path = ROOT/'manual'/f'C_escala50_{name}.csv'
    return read(path)

def comparison(a, b, factor=1):
    common = sorted(set(a)&set(b))
    assert common
    mismatches = {}
    max_errors = {}
    for col in COLS:
        scale = factor if col != 'Volume' else 1
        errors = []
        missing = 0
        for t in common:
            x,y = a[t][col],b[t][col]
            if bool(x)!=bool(y): missing+=1
            elif x and y: errors.append(abs(float(y)-scale*float(x)))
        mismatches[col] = missing+sum(e!=0 for e in errors)
        max_errors[col] = max(errors,default=None)
    return {'common_closed_bars':len(common),'mismatches':mismatches,'max_errors':max_errors}

def measurement(rows):
    stamps = list(range(START,END+1,60))
    assert all(t in rows for t in stamps)
    # Una hora posterior, dentro de la misma sesión (evita pausa diaria a 21:00 UTC).
    assert all(t in rows for t in range(END+60,END+3660,60))
    fits = fit_lite(rows,60,60)
    cs = [v['C'] for v in fits.values()]
    assert max(cs)-min(cs)<1e-6
    assert max(v['rmse'] for v in fits.values())<1e-8
    return {'C':sum(cs)/len(cs),'range_bars':len(stamps),
            'range_high':max(float(rows[t]['high']) for t in stamps),
            'range_low':min(float(rows[t]['low']) for t in stamps),
            'six_curve_fits':fits}

def main():
    names = ['base_a','base_b','identidad_alternativa_a','identidad_alternativa_b','doble_a','doble_b','regreso']
    data = {n:load(n) for n in names}
    out = {
      'START_UTC':'2026-10-12T19:02:00Z','END_UTC':'2026-10-12T19:22:00Z',
      'source_seconds':60,'chart_seconds':60,'indicator':'Lite v1.2',
      'original_control':'NQ1!+0 normalized to native symbol; rejected as synthetic control',
      'alternative_control':'(CME_MINI:NQ1!+CME_MINI:NQ1!)/2 retained in chart export dialog',
      'double_symbol':'2*CME_MINI:NQ1! retained in chart export dialog',
      'measurements':{n:measurement(data[n]) for n in ['base_b','identidad_alternativa_b','doble_b','regreso']},
      'checks':{
        'base_repeat':comparison(data['base_a'],data['base_b']),
        'identity_vs_native':comparison(data['base_b'],data['identidad_alternativa_b']),
        'identity_earlier_export':comparison(data['identidad_alternativa_a'],data['identidad_alternativa_b']),
        'double_vs_native':comparison(data['base_b'],data['doble_b'],2),
        'double_repeat':comparison(data['doble_a'],data['doble_b']),
        'return_vs_native':comparison(data['base_b'],data['regreso'])},
      'sha256':{n:hashlib.sha256((ROOT/'manual'/f'C_escala50_{n}.csv').read_bytes()).hexdigest() for n in names},
      'predeclared_predictions':{'scale_invariant':50,'Gemini_v4':77},
      'interpretation':'C remains 50 under price doubling in this window. Gemini v4 transformed-price prediction 77 fails. This does not identify the generator or establish harmonic alignment.',
      'limits':'Alternative identity was an exploratory compatibility repair declared before measuring it. Metadata/history context is not fully observable; inference concerns chart OHLCV and plotted Lite recurrence. Character updated externally and excluded.'}
    assert all(all(n==0 for n in c['mismatches'].values()) for c in out['checks'].values())
    assert all(abs(v['C']-50)<1e-6 for v in out['measurements'].values())
    (ROOT/'C_escala50_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'C':{n:v['C'] for n,v in out['measurements'].items()},'comparisons':{n:v['common_closed_bars'] for n,v in out['checks'].items()},'all_checks_passed':True},indent=2))

if __name__=='__main__':main()
