"""Valida todos los conteos21..40; distingue predicciones de acotación."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from analizar_C_frontera_1s import read, BASES
from analizar_C_fuente_vs_grafico import fit_lite, LANES

ROOT = Path(__file__).parent


def main():
    spec = json.loads((ROOT/'C_1S_SALIDA_MESETA_PREREGISTRO.json').read_text())
    extra = json.loads((ROOT/'C_1S_MESETA_HUECOS_PREREGISTRO.json').read_text())
    start = int(datetime.fromisoformat(spec['START_UTC'].replace('Z','+00:00')).timestamp())
    results = []
    for n in range(21,41):
        prefix = 'C_1s_r1404_n21' if n==21 else f'C_1s_plateau_n{n}'
        paths = [ROOT/'manual'/f'{prefix}_{s}.csv' for s in ['a','b']]
        a,b = [read(p) for p in paths]
        common = sorted(set(a)&set(b))
        columns = ['open','high','low','close','Volume']+LANES
        assert common and all(a[t][k]==b[t][k] for t in common for k in columns), f'n{n}: unstable'
        end = start+n-1
        assert all(t in a and t in b for t in range(start,end+601)), f'n{n}: missing1s'
        rows = [{k:(t if k=='time' else float(b[t][k])) for k in ['time','open','high','low','close','Volume']} for t in range(start,end+1)]
        fits = fit_lite(b,1,1)
        C = sum(f['C'] for f in fits.values())/6
        assert max(f['C'] for f in fits.values())-min(f['C'] for f in fits.values())<1e-6
        assert max(f['rmse'] for f in fits.values())<1e-8
        assert min(f['pairs'] for f in fits.values())>=5
        high,low = max(r['high'] for r in rows), min(r['low'] for r in rows)
        first_break = next(t for t in range(end+1,end+601) if float(b[t]['close'])>high or float(b[t]['close'])<low)
        up = float(b[first_break]['close'])>high
        seed = float(b[end]['low' if up else 'high'])
        state = dict.fromkeys(LANES,seed)
        alphas = {k:2/(base*C+1) for k,base in BASES.items()}
        errors = []
        visibility_errors = 0
        for t in range(end+1,end+601):
            for k in LANES:
                state[k] += alphas[k]*(float(b[t]['close'])-state[k])
                visibility_errors += bool(b[t][k]) != (t>=first_break)
                if b[t][k]: errors.append(abs(state[k]-float(b[t][k])))
        assert visibility_errors==0 and errors and max(errors)<1e-8, f'n{n}: reconstruction'
        prior_prediction = 1 if n in spec['initial_counts'] or n in extra['counts'] else None
        result = {'bars':n,'START_UTC':spec['START_UTC'],'END_UTC':datetime.fromtimestamp(end,timezone.utc).isoformat(),
            'C':C,'prediction_C':prior_prediction,'prediction_matches':None if prior_prediction is None else abs(C-prior_prediction)<1e-6,
            'OHLC':rows,'high':high,'low':low,'END_OHLCV':rows[-1],
            'seed':seed,'first_break_timestamp':first_break,'breakout_direction':'up' if up else 'down',
            'fits':fits,'repeat_cells':len(common)*len(columns),'reconstruction_values':len(errors),
            'max_reconstruction_error':max(errors),'visibility_errors':visibility_errors,
            'files':[str(p) for p in paths],'SHA256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]}
        if results: assert results[-1]['OHLC']==rows[:-1]
        results.append(result)
    repeat_a,repeat_b = [read(ROOT/'manual'/f'C_1s_plateau_n33_{s}.csv') for s in ['c','d']]
    original = read(ROOT/'manual'/'C_1s_plateau_n33_b.csv')
    for replica in [repeat_a,repeat_b]:
        common = set(original)&set(replica)
        assert common and all(original[t][k]==replica[t][k] for t in common for k in columns), '33 repeat differs'
    assert max(abs(f['C']-2) for f in fit_lite(repeat_b,1,1).values())<1e-6
    out = {'initial_spec':spec,'supplementary_spec':extra,'results':results,
        'n33_return_repeat_verified':True,
        'first_non_one_count':next(r['bars'] for r in results if abs(r['C']-1)>1e-6),
        'initial_predictions_correct':sum(r['prediction_matches'] is True for r in results if r['bars'] in spec['initial_counts']),
        'supplementary_predictions_correct':sum(r['prediction_matches'] is True for r in results if r['bars'] in extra['counts']),
        'scope':'Twenty counts from one episode; n21 inherited from previous replica. Nineteen new selections. No claim of universal floor or integerC. No independent Character corroboration.'}
    (ROOT/'C_1s_salida_meseta_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ['bars','C','high','low','first_break_timestamp','breakout_direction','max_reconstruction_error']} for r in results],indent=2))
    print('First non-one count:',out['first_non_one_count'])


if __name__=='__main__': main()
