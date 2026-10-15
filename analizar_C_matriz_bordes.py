"""Audita las dos esquinas nuevas y reúne matriz3x3, sin ajustar modelo."""
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
from analizar_C_frontera_1s import read
from analizar_C_fuente_vs_grafico import fit_lite,LANES
from analizar_C_traslacion50 import comparison
from analizar_C_bordes26 import stamp

ROOT=Path(__file__).parent

def main():
    spec=json.loads((ROOT/'C_MATRIZ_BORDES_PREREGISTRO.json').read_text())
    prior=json.loads((ROOT/'C_bordes26_resultados.json').read_text())['results']
    sweep=json.loads((ROOT/'C_startSweep1920_resultados.json').read_text())['results']
    grid={(r['START'],r['END']):r for r in prior}
    for r in sweep:
        if r['START'] in ['18:54','18:55','18:56']:
            grid.setdefault((r['START'],'19:20'),{**r,'END':'19:20'})
    baseline=read(ROOT/'manual/C_simetria1855_base.csv')
    new=[]
    hashes={}
    for case in spec['new_cases']:
        s,e=stamp(case['START']),stamp(case['END'])
        paths=[ROOT/'manual'/f'C_startSweep1920_bordes_{case["id"]}_{suffix}.csv' for suffix in ['a','b']]
        a,b=[read(p) for p in paths]
        repeated=comparison(a,b)
        common=set(baseline)&set(b)
        assert all(baseline[t][k]==b[t][k] for t in common for k in ['open','high','low','close','Volume'])
        window=list(range(s,e+1,60))
        assert len(window)==case['n'] and all(t in b for t in window)
        assert all(t in b for t in range(e+60,e+3660,60))
        fits=fit_lite(b,60,60)
        cs=[v['C'] for v in fits.values()]
        assert max(cs)-min(cs)<1e-6 and max(v['rmse'] for v in fits.values())<1e-8
        hi=max(float(b[t]['high']) for t in window)
        lo=min(float(b[t]['low']) for t in window)
        rupture=next(t for t in range(e+60,e+3660,60) if float(b[t]['close'])>hi or float(b[t]['close'])<lo)
        bull=float(b[rupture]['close'])>hi
        assert all(min(t for t,r in b.items() if t>e and r[k])==rupture for k in LANES)
        result={**case,'C':sum(cs)/6,'H':hi,'L':lo,'rupture_UTC':datetime.fromtimestamp(rupture,timezone.utc).isoformat(),
                'direction':'bull' if bull else 'bear','seed':float(b[e]['low' if bull else 'high']),
                'START_OHLC':{k:float(b[s][k]) for k in ['open','high','low','close']},
                'END_OHLC':{k:float(b[e][k]) for k in ['open','high','low','close']},
                'repeat_common_bars':repeated['common_closed_bars'],'native_common_bars':len(common),'fits':fits}
        new.append(result)
        grid[(case['START'],case['END'])]=result
        hashes.update({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    starts=['18:54','18:55','18:56'];ends=['19:19','19:20','19:21']
    assert len(grid)==9
    # Rounded presentation only after independently inferred C values are confirmed near integers.
    assert all(abs(r['C']-round(r['C']))<1e-6 for r in grid.values())
    C=[[round(grid[(s,e)]['C']) for e in ends] for s in starts]
    interactions=[[C[i+1][j+1]-C[i+1][j]-C[i][j+1]+C[i][j] for j in range(2)] for i in range(2)]
    path=ROOT/'manual/C_startSweep1920_matriz_regreso.csv'
    ret=read(path);back=comparison(baseline,ret);return_fits=fit_lite(ret,60,60)
    assert all(abs(v['C']-62)<1e-6 for v in return_fits.values())
    hashes[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    out={'preregistered':spec,'new_results':new,'starts':starts,'ends':ends,'C_matrix':C,
         'all_cases':[grid[(s,e)] for s in starts for e in ends],'mixed_differences':interactions,
         'return_check':back,'return_fits':return_fits,'new_sha256':hashes,
         'interpretation':'Count-only and additive C=f(START)+g(END) are incompatible with the observed matrix. This does not identify harmonics, causal variable or pre-START anchor.'}
    (ROOT/'C_matriz_bordes_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'new_results':[{k:r[k] for k in ['START','END','n','C','H','L','rupture_UTC','seed']} for r in new],'C_matrix':C,'mixed_differences':interactions,'return_verified':True},indent=2))

if __name__=='__main__':main()
