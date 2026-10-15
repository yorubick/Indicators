"""Control de frontera START exacta con fuente fija de 15 segundos."""
import csv,json
from pathlib import Path
from datetime import datetime,timezone
from obtener_C import recover
ROOT=Path(__file__).parent
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        return {int(r['time']):r for r in list(csv.DictReader(f))[:-1]}
def main():
    results=[];datasets=[]
    for time in ['185415','185416','185429','185430']:
        prefix=ROOT/'manual'/('C_limite_'+time)
        a,b=Path(str(prefix)+'_a.csv'),Path(str(prefix)+'_b.csv')
        x,y=recover(a),recover(b);assert x['periods']==y['periods']
        ra,rb=read(a),read(b);keys=list(x['periods'])
        common=sorted(set(ra)&set(rb))[:-1]
        assert all(ra[t][k]==rb[t][k] for t in common for k in keys)
        start=int(datetime.fromisoformat('2026-10-12T'+':'.join([time[:2],time[2:4],time[4:]])+'+00:00').timestamp())
        end=int(datetime.fromisoformat('2026-10-12T19:20:00+00:00').timestamp())
        expected=list(range(((start+14)//15)*15,end+1,15))
        assert all(t in rb for t in expected)
        seg=[rb[t] for t in expected]
        results.append({'START_UTC':datetime.fromtimestamp(start,timezone.utc).isoformat(),
            'effective_first_source_bar_UTC':datetime.fromtimestamp(expected[0],timezone.utc).isoformat(),
            'source_bar_count':len(expected),'range_high':max(float(r['high']) for r in seg),
            'range_low':min(float(r['low']) for r in seg),'extraction':y,
            'repeated_values_checked':len(common)*len(keys)})
        datasets.append(rb)
    base=datasets[1];common=sorted(set.intersection(*(set(r) for r in datasets[1:])))[:-1]
    equality=all(base[t][k]==r[t][k] for r in datasets[2:] for t in common for k in keys)
    assert equality
    out={'cases':results,'plots_16_29_30_identical':equality,
        'scope':'Perfil B Manual, fuente fija 15s, NQ1!, 2026-10-12. Anclas finas colocadas en grafico 1s y preservadas al cambiar resolucion. C recuperado de plots, no generado desde OHLC.'}
    (ROOT/'C_limite_segundo.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
