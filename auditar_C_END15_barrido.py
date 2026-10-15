"""Audita el barrido preregistrado de nueve END nativos de 15s."""
import json,hashlib
from pathlib import Path
from analizar_C_frontera_1s import read
from analizar_C_fuente_vs_grafico import fit_lite,LANES
from analizar_C_traslacion50 import comparison
from analizar_C_bordes26 import stamp

ROOT=Path(__file__).parent
BASES=dict(zip(LANES,[24,89/3,8,89/9,72/27,89/27]))

def main():
    spec=json.loads((ROOT/'C_END15_BARRIDO_PREREGISTRO.json').read_text())
    s=stamp('18:52');results=[];hashes={}
    native=read(ROOT/'manual/C_estructura15_A_last_base_b.csv')
    for end in spec['END_UTC']:
        name=end.replace(':','');e=stamp(end[:5])+int(end[-2:])
        paths=[ROOT/'manual'/f'C_estructura15_barrido_{name}_{suffix}.csv' for suffix in ['a','b']]
        a,b=[read(p) for p in paths];rep=comparison(a,b)
        assert all(t in b for t in range(s,e+3601,15))
        scope={t:b[t] for t in range(s,e+3601,15)}
        price_comparison={}
        for k in ['open','high','low','close','Volume']:
            errors=[abs(float(row[k])-float(native[t][k])) for t,row in scope.items()]
            assert max(errors)==0
            price_comparison[k]=max(errors)
        fits=fit_lite(b,15,15);cs=[x['C'] for x in fits.values()];C=sum(cs)/6
        assert max(cs)-min(cs)<1e-6 and max(x['rmse'] for x in fits.values())<1e-8
        window=list(range(s,e+1,15));hi=max(float(b[t]['high']) for t in window);lo=min(float(b[t]['low']) for t in window)
        rupture=next(t for t in range(e+15,e+3601,15) if float(b[t]['close'])>hi or float(b[t]['close'])<lo)
        bull=float(b[rupture]['close'])>hi;seed=float(b[e]['low' if bull else 'high']);values=dict.fromkeys(LANES,seed);errs=[];vis=0
        for t in range(e+15,e+3601,15):
            for lane,base in BASES.items():
                values[lane]+=2/(base*C/15+1)*(float(b[t]['close'])-values[lane])
                vis+=bool(b[t][lane])!=(t>=rupture)
                if b[t][lane]:errs.append(abs(values[lane]-float(b[t][lane])))
        assert vis==0 and max(errs)<1e-8
        if end in spec['controls']:assert abs(C-spec['controls'][end])<1e-6
        results.append({'END':end,'n':len(window),'C':C,'delta_C':None if not results else C-results[-1]['C'],
                        'H':hi,'L':lo,'seed':seed,'rupture_timestamp':rupture,'END_OHLCV':{k:float(b[e][k]) for k in ['open','high','low','close','Volume']},
                        'pair_common_bars':rep['common_closed_bars'],'native_price_max_errors':price_comparison,
                        'fits':fits,'reconstruction_max_error':max(errs),'visibility_errors':vis})
        hashes.update({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    out={'spec':spec,'results':results,'sha256':hashes,'status':'all nine cases passed'}
    retpath=ROOT/'manual/C_estructura15_barrido_regreso_1m.csv'
    if retpath.exists():
        ret=read(retpath);assert all(t in ret for t in range(stamp('18:55'),stamp('19:20')+3601,60))
        out['return_check']=comparison(read(ROOT/'manual/C_estructura_regreso_final.csv'),ret)
        out['return_fits']=fit_lite(ret,60,60);assert all(abs(v['C']-62)<1e-6 for v in out['return_fits'].values())
    (ROOT/'C_END15_barrido_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ['END','n','C','delta_C','H','L','seed','END_OHLCV']} for r in results],indent=2))

if __name__=='__main__':main()
