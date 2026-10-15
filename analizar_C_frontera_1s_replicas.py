"""Verifica cuatro réplicas prospectivas1s; no estima una fórmula generalC."""
import hashlib
import json
from datetime import datetime
from pathlib import Path

from analizar_C_frontera_1s import read, BASES
from analizar_C_fuente_vs_grafico import fit_lite, LANES

ROOT = Path(__file__).parent


def stamp(value):
    return int(datetime.fromisoformat(value.replace('Z','+00:00')).timestamp())


def main():
    spec = json.loads((ROOT/'C_FRONTERA_1S_REPLICAS_PREREGISTRO.json').read_text())
    results = []
    for case in spec['cases']:
        paths = [ROOT/'manual'/f"C_1s_{case['id']}_{s}.csv" for s in ['a','b']]
        first, second = [read(p) for p in paths]
        common = sorted(set(first)&set(second))
        cols = ['open','high','low','close','Volume']+LANES
        assert common and all(first[t][k]==second[t][k] for t in common for k in cols), 'unstable exports'
        start, end = stamp(case['START_UTC']), stamp(case['END_UTC'])
        assert end-start+1 == case['bars']
        assert all(t in first and t in second for t in range(start,end+601)), 'incomplete native1s coverage'
        rows = [{k:(t if k=='time' else float(second[t][k])) for k in ['time','open','high','low','close','Volume']} for t in range(start,end+1)]
        fits = fit_lite(second,1,1)
        C = sum(f['C'] for f in fits.values())/6
        assert max(f['C'] for f in fits.values())-min(f['C'] for f in fits.values()) < 1e-6
        assert max(f['rmse'] for f in fits.values())<1e-8
        assert min(f['pairs'] for f in fits.values())>=5
        high, low = max(r['high'] for r in rows), min(r['low'] for r in rows)
        breakout = next(t for t in range(end+1,end+601) if float(second[t]['close'])>high or float(second[t]['close'])<low)
        bullish = float(second[breakout]['close'])>high
        seed = float(second[end]['low' if bullish else 'high'])
        state = dict.fromkeys(LANES,seed)
        alphas = {lane:2/(base*C+1) for lane,base in BASES.items()}
        errors = []
        visible_errors = 0
        for t in range(end+1,end+601):
            for lane in LANES:
                state[lane] += alphas[lane]*(float(second[t]['close'])-state[lane])
                visible = bool(second[t][lane])
                visible_errors += visible != (t>=breakout)
                if visible:
                    errors.append(abs(state[lane]-float(second[t][lane])))
        assert visible_errors==0 and errors and max(errors)<1e-8, 'seed/publication discrepancy'
        results.append(case | {'C':C,'prediction_matches':abs(C-case['prediction_C'])<1e-6,
             'OHLC':rows,'Lite_fits':fits,'files':[str(p) for p in paths],
             'SHA256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths],
             'repeat_cells':len(common)*len(cols),'high':high,'low':low,
             'start_open':rows[0]['open'],'end_close':rows[-1]['close'],
             'END_seed':seed,'breakout_timestamp':breakout,'breakout_direction':'up' if bullish else 'down',
             'reconstruction_values':len(errors),'reconstruction_max_error':max(errors),'visibility_errors':visible_errors})
    assert results[0]['OHLC']==results[1]['OHLC'][:20]
    assert results[2]['OHLC']==results[3]['OHLC'][:20]
    out = {'spec':spec,'results':results,'exact_predictions':sum(r['prediction_matches'] for r in results),
           'scope':'Six Lite estimates; no independent Character corroboration. Two new ranges, same market/session; possible floor/quantization ofC1 remains unresolved. No replay/forced direction test executed.'}
    (ROOT/'C_frontera_1s_replicas_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ['id','C','prediction_matches','repeat_cells','high','low','start_open','end_close','breakout_direction','reconstruction_max_error']} for r in results],indent=2))


if __name__ == '__main__':
    main()
