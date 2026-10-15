"""Compara cortes de replay; no equipara ausencia de plot con C cero."""
import csv,json
from pathlib import Path
from datetime import datetime,timezone
from obtener_C import recover
from identificar_emas import COLUMNS
ROOT=Path(__file__).parent
def stamp(s):return int(datetime.fromisoformat('2026-10-12T'+s+':00+00:00').timestamp())
def read(name):
    with (ROOT/name).open(encoding='utf-8-sig') as f:return {int(r['time']):r for r in csv.DictReader(f)}
def main():
    reference=read('C_historial_1854_1920_antes.csv');out=[]
    for cut in ('1926','1927','1931','1933','1940'):
        name=f'C_historial_replay_{cut}.csv';data=read(name)
        cutoff=stamp(cut[:2]+':'+cut[2:])
        assert max(data)==cutoff-60,'Ultima vela exportada no coincide con corte solicitado'
        common=reference.keys() & data.keys()
        last=max(data)
        assert all(reference[t][k]==data[t][k] for t in common if t<last for k in ('open','high','low','close'))
        # En estos cortes, el ultimo OHLC existe pero sus plots repiten el estado
        # de la vela anterior. Se documenta aparte, no se compara como confirmado.
        pairs=[(float(reference[t][k]),float(data[t][k])) for t in common for k in COLUMNS if t<last and data[t].get(k) and reference[t].get(k)]
        assert all(x==y for x,y in pairs)
        values=sum(bool(r.get(k)) for t,r in data.items() for k in COLUMNS if t<last)
        assert values==len(pairs)
        first=min((t for t,r in data.items() if r.get('Layer A')),default=None)
        record={'cutoff_UTC':cut[:2]+':'+cut[2:],'file':name,'last_bar_UTC':datetime.fromtimestamp(max(data),timezone.utc).isoformat(),
            'first_visible_UTC':datetime.fromtimestamp(first,timezone.utc).isoformat() if first else None,
            'matching_confirmed_curve_values':values,'max_confirmed_curve_difference':0 if pairs else None,
            'last_row_numeric_curve_values':sum(bool(data[last].get(k)) for k in COLUMNS),
            'last_row_matches_previous_reference_plots':all(data[last].get(k)==reference[last-60].get(k) for k in COLUMNS),
            'last_row_OHLC':{k:data[last][k] for k in ('open','high','low','close')},
            'last_row_final_reference_OHLC':{k:reference[last][k] for k in ('open','high','low','close')}}
        assert record['last_row_matches_previous_reference_plots']
        try:record['extraction']=recover(ROOT/name)
        except (ValueError,KeyError,StopIteration) as e:record['extraction_unavailable_reason']=str(e)
        if 'extraction' in record:assert record['extraction']['compatible_integer_C_seconds']==[134]
        out.append(record)
    (ROOT/'C_replay_temprano.json').write_text(json.dumps({'scope':'Valores historicos y C Manual en estos cortes; no auditoria completa de repintado.','cases':out},indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in c.items() if k!='extraction'}|{'C':c.get('extraction',{}).get('compatible_integer_C_seconds')} for c in out],indent=2))
if __name__=='__main__':main()
