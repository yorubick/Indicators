"""Valida los CSV nativos1s contra el preregistro y reconstruye Lite."""
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path

from analizar_C_fuente_vs_grafico import fit_lite, LANES

ROOT = Path(__file__).parent
BASES = dict(zip(LANES, [24,89/3,8,89/9,72/27,89/27]))


def read(path):
    with path.open(encoding='utf-8-sig', newline='') as source:
        rows = list(csv.DictReader(source))[:-1]
    assert len({int(r['time']) for r in rows}) == len(rows)
    return {int(r['time']):r for r in rows}


def main():
    spec = json.loads((ROOT/'C_FRONTERA_1S_PREREGISTRO.json').read_text())
    start = int(datetime.fromisoformat(spec['START_UTC'].replace('Z','+00:00')).timestamp())
    results = []
    sources = {}
    for expected in spec['cases']:
        n = expected['bars']
        suffixes = ['c','d'] if n==21 else ['a','b']
        paths = [ROOT/'manual'/f'C_1s_{n}_{suffix}.csv' for suffix in suffixes]
        first, second = [read(p) for p in paths]
        common = sorted(set(first)&set(second))
        columns = ['open','high','low','close','Volume']+LANES
        assert common and all(first[t][k]==second[t][k] for t in common for k in columns), 'unstable exports'
        end = start+n-1
        assert expected['END_UTC'] == datetime.fromtimestamp(end,datetime.fromisoformat('2026-10-14T00:00:00+00:00').tzinfo).isoformat().replace('+00:00','Z')
        assert all(t in second for t in range(start,end+1)), 'missing range timestamps'
        window = [{k:(int(second[t][k]) if k=='time' else float(second[t][k])) for k in ['time','open','high','low','close','Volume']} for t in range(start,end+1)]
        fits = fit_lite(second,1,1)
        C = sum(f['C'] for f in fits.values())/6
        assert max(f['C'] for f in fits.values())-min(f['C'] for f in fits.values()) < 1e-6
        assert max(f['rmse'] for f in fits.values()) <= 1e-8
        assert min(f['pairs'] for f in fits.values())>=5
        high = max(r['high'] for r in window)
        low = min(r['low'] for r in window)
        horizon = end+600
        assert all(t in second for t in range(end+1,horizon+1)), 'missing forward samples'
        rupture = next(t for t in range(end+1,horizon+1) if float(second[t]['close'])>high or float(second[t]['close'])<low)
        bullish = float(second[rupture]['close'])>high
        seed = float(second[end]['low' if bullish else 'high'])
        values = dict.fromkeys(LANES,seed)
        alphas = {lane:2/(base*C+1) for lane,base in BASES.items()}
        errors = []
        visibility_errors = 0
        for t in range(end+1,horizon+1):
            for lane in LANES:
                values[lane] += alphas[lane]*(float(second[t]['close'])-values[lane])
                visible = bool(second[t][lane])
                visibility_errors += visible != (t>=rupture)
                if visible:
                    errors.append(abs(values[lane]-float(second[t][lane])))
        assert visibility_errors==0, 'unexpected plot visibility'
        assert errors and max(errors)<1e-8, 'seed or recurrence differs'
        original = read(ROOT/'manual'/f'C_1s_{n}_a.csv')
        older_common = set(original)&set(second)
        assert all(original[t][k]==second[t][k] for t in older_common for k in columns), 'return differs'
        if n==20:
            returned = read(ROOT/'manual'/'C_1s_20_return_b.csv')
            return_common = set(returned)&set(second)
            assert all(returned[t][k]==second[t][k] for t in return_common for k in columns), '20 return differs'
        result = expected | {'C':C,'OHLC':window,'Lite_fits':fits,
            'files':[str(p) for p in paths],
            'file_SHA256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths],
            'repeat_cells':len(common)*len(columns),
            'range_high':high,'range_low':low,'END_seed':seed,'breakout_time':rupture,
            'breakout_direction':'up' if bullish else 'down',
            'reconstruction_values':len(errors),'reconstruction_max_error':max(errors),
            'visibility_errors':visibility_errors}
        results.append(result)
        sources[n] = second
    assert results[0]['OHLC']==results[1]['OHLC'][:19]
    assert results[1]['OHLC']==results[2]['OHLC'][:20]
    out = {'spec':spec,'results':results,'scope':'Lite original v1.2 loaded; update available not applied. Character reference anchors remained12oct and produced a data-coverage error, so Character was not used to corroborate this1s test. No indication of hiddenCbeforebreakout.',
           'measurement_date':'2026-10-14', 'same_prefix_verified':True}
    (ROOT/'C_frontera_1s_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ['bars','END_UTC','C','repeat_cells','reconstruction_max_error','visibility_errors']} for r in results],indent=2))


if __name__ == '__main__':
    main()
