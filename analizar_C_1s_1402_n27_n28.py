"""Dos controles prospectivos de la fórmula round(n/18.3)."""
import hashlib
import json
from datetime import datetime
from pathlib import Path

from analizar_C_frontera_1s import read, BASES
from analizar_C_fuente_vs_grafico import fit_lite, LANES

ROOT=Path(__file__).parent


def main():
    spec=json.loads((ROOT/'C_1S_1402_N27_N28_PREREGISTRO.json').read_text())
    start=int(datetime.fromisoformat(spec['START_UTC'].replace('Z','+00:00')).timestamp())
    results=[]
    for case in spec['cases']:
        paths=[ROOT/'manual'/f"C_1s_{case['id']}_{s}.csv" for s in ['a','b']]
        a,b=[read(p) for p in paths]
        common=sorted(set(a)&set(b));cols=['open','high','low','close','Volume']+LANES
        assert common and all(a[t][k]==b[t][k] for t in common for k in cols), 'unstable exports'
        end=int(datetime.fromisoformat(case['END_UTC'].replace('Z','+00:00')).timestamp())
        assert end-start+1==case['bars'] and all(t in a and t in b for t in range(start,end+601))
        rows=[{k:(t if k=='time' else float(b[t][k])) for k in ['time','open','high','low','close','Volume']} for t in range(start,end+1)]
        fits=fit_lite(b,1,1);C=sum(f['C'] for f in fits.values())/6
        assert max(f['C'] for f in fits.values())-min(f['C'] for f in fits.values())<1e-6
        assert max(f['rmse'] for f in fits.values())<1e-8 and min(f['pairs'] for f in fits.values())>=5
        high,low=max(r['high'] for r in rows),min(r['low'] for r in rows)
        breakout=next(t for t in range(end+1,end+601) if float(b[t]['close'])>high or float(b[t]['close'])<low)
        seed=float(b[end]['low' if float(b[breakout]['close'])>high else 'high'])
        state=dict.fromkeys(LANES,seed);alphas={k:2/(base*C+1) for k,base in BASES.items()}
        errors=[];visibility_errors=0
        for t in range(end+1,end+601):
            for k in LANES:
                state[k]+=alphas[k]*(float(b[t]['close'])-state[k])
                visibility_errors+=bool(b[t][k])!=(t>=breakout)
                if b[t][k]: errors.append(abs(state[k]-float(b[t][k])))
        assert visibility_errors==0 and errors and max(errors)<1e-8
        results.append(case|{'C':C,'residual_C_minus_prediction':C-case['prediction_C'],
            'prediction_matches':abs(C-case['prediction_C'])<1e-6,
            'OHLC':rows,'fits':fits,'high':high,'low':low,'breakout_timestamp':breakout,'seed':seed,
            'repeat_cells':len(common)*len(cols),'reconstruction_values':len(errors),
            'max_reconstruction_error':max(errors),'visibility_errors':visibility_errors,
            'files':[str(p) for p in paths],'SHA256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]})
    assert results[0]['OHLC']==results[1]['OHLC'][:-1]
    out={'spec':spec,'results':results,'matches':sum(r['prediction_matches'] for r in results),
         'scope':'Same market/session, six Lite curves without independent Character corroboration. Rejects only the literal proposed formula; integer outputs do not prove a quantum grid.'}
    (ROOT/'C_1s_1402_n27_n28_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ['bars','prediction_C','C','prediction_matches','repeat_cells','max_reconstruction_error']} for r in results],indent=2))


if __name__=='__main__':main()
