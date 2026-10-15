"""Cruce nuevo START01 con dos END, controles START00 ya verificados."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from analizar_C_frontera_1s import read, BASES
from analizar_C_fuente_vs_grafico import fit_lite, LANES

ROOT = Path(__file__).parent


def main():
    spec = json.loads((ROOT/'C_1S_CRUCE_START_PREREGISTRO.json').read_text())
    previous = json.loads((ROOT/'C_1s_salida_meseta_resultados.json').read_text())
    controls = [r for r in previous['results'] if r['bars'] in [33,34]]
    start = int(datetime.fromisoformat(spec['START_UTC'].replace('Z','+00:00')).timestamp())
    results = []
    for expected, control in zip(spec['cases'],controls):
        paths = [ROOT/'manual'/f"C_1s_{expected['id']}_{s}.csv" for s in ['a','b']]
        a,b = [read(p) for p in paths]
        common = sorted(set(a)&set(b))
        columns = ['open','high','low','close','Volume']+LANES
        assert common and all(a[t][k]==b[t][k] for t in common for k in columns), 'unstable'
        end = int(datetime.fromisoformat(expected['END_UTC'].replace('Z','+00:00')).timestamp())
        assert end-start+1==expected['bars']
        assert all(t in a and t in b for t in range(start,end+601)), 'missing native1s'
        rows = [{k:(t if k=='time' else float(b[t][k])) for k in ['time','open','high','low','close','Volume']} for t in range(start,end+1)]
        assert rows==control['OHLC'][1:], 'selected range differs from original suffix'
        fits = fit_lite(b,1,1)
        C = sum(f['C'] for f in fits.values())/6
        assert max(f['C'] for f in fits.values())-min(f['C'] for f in fits.values())<1e-6
        assert max(f['rmse'] for f in fits.values())<1e-8
        assert min(f['pairs'] for f in fits.values())>=5
        high,low = max(r['high'] for r in rows),min(r['low'] for r in rows)
        breakout = next(t for t in range(end+1,end+601) if float(b[t]['close'])>high or float(b[t]['close'])<low)
        up = float(b[breakout]['close'])>high
        seed = float(b[end]['low' if up else 'high'])
        state = dict.fromkeys(LANES,seed)
        alphas = {k:2/(base*C+1) for k,base in BASES.items()}
        errors = []
        visibility_errors = 0
        for t in range(end+1,end+601):
            for k in LANES:
                state[k] += alphas[k]*(float(b[t]['close'])-state[k])
                visibility_errors += bool(b[t][k]) != (t>=breakout)
                if b[t][k]: errors.append(abs(state[k]-float(b[t][k])))
        assert visibility_errors==0 and errors and max(errors)<1e-8
        original = read(Path(control['files'][1]))
        market_common = set(original)&set(b)
        assert market_common and all(original[t][k]==b[t][k] for t in market_common for k in ['open','high','low','close','Volume'])
        results.append(expected | {'START_UTC':spec['START_UTC'],'C':C,'OHLC':rows,
            'count_residual_C_minus_prediction':C-expected['prediction_count_only'],
            'END_residual_C_minus_prediction':C-expected['prediction_END_only'],
            'high':high,'low':low,'breakout_timestamp':breakout,'breakout_UTC':datetime.fromtimestamp(breakout,timezone.utc).isoformat(),
            'seed':seed,'fits':fits,'repeat_cells':len(common)*len(columns),
            'reconstruction_values':len(errors),'max_reconstruction_error':max(errors),
            'visibility_errors':visibility_errors,'files':[str(p) for p in paths],
            'SHA256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths],
            'extrema_conserved':high==control['high'] and low==control['low'],
            'breakout_conserved':breakout==control['first_break_timestamp'],
            'seed_conserved':seed==control['seed'],
            'count_prediction_matches':abs(C-expected['prediction_count_only'])<1e-6,
            'END_prediction_matches':abs(C-expected['prediction_END_only'])<1e-6})
    assert results[0]['OHLC']==results[1]['OHLC'][:-1]
    out = {'spec':spec,'results':results,
           'controls':[{k:r[k] for k in ['START_UTC','END_UTC','bars','C','high','low','first_break_timestamp','seed']} for r in controls],
           'count_model_matches':sum(r['count_prediction_matches'] for r in results),
           'END_model_matches':sum(r['END_prediction_matches'] for r in results),
           'difference_of_differences':(controls[1]['C']-controls[0]['C'])-(results[1]['C']-results[0]['C']),
           'scope':'Two new prospective controls same episode; interaction constraint does not identify mechanism. No independent Character corroboration.'}
    (ROOT/'C_1s_cruce_START_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ['id','bars','C','high','low','breakout_UTC','extrema_conserved','breakout_conserved','seed_conserved','max_reconstruction_error']} for r in results],indent=2))


if __name__=='__main__': main()
