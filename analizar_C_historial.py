"""Control empirico de historial cargado: no demuestra ausencia de toda dependencia pasada."""
import csv,json
from pathlib import Path
from datetime import datetime,timezone
from obtener_C import recover
from identificar_emas import COLUMNS
ROOT=Path(__file__).parent
def stamp(t):return int(datetime.fromisoformat('2026-10-12T'+t+'+00:00').timestamp())
def read(name):
    with (ROOT/name).open(encoding='utf-8-sig') as f:return {int(r['time']):r for r in csv.DictReader(f)}
def main():
    files=['C_historial_1854_1920_antes.csv','C_historial_1854_1920_ampliado.csv','C_historial_1854_1920_recargado.csv']
    rows=[read(f) for f in files];out=[]
    reference=rows[0];start=stamp('18:54:00');end=stamp('19:20:00')
    target=list(range(start,end+1,60))
    for name,data in zip(files,rows):
        assert all(t in data for t in target)
        assert all(reference[t][k]==data[t][k] for t in target for k in ('open','high','low','close'))
        compared=sorted(t for t in reference.keys() & data.keys() if stamp('19:22:00')<=t<stamp('20:40:00'))
        errors=[abs(float(reference[t][k])-float(data[t][k])) for t in compared for k in COLUMNS if reference[t][k] and data[t][k]]
        assert errors and max(errors)==0
        fit=recover(ROOT/name)
        assert fit['compatible_integer_C_seconds']==[134]
        first=min(data)
        out.append({'file':name,'loaded_rows':len(data),'first_loaded_UTC':datetime.fromtimestamp(first,timezone.utc).isoformat(),
            'loaded_bars_before_START':sum(t<start for t in data),'range_OHLC_identical':True,
            'comparison_values':len(errors),'max_curve_difference':max(errors),'extraction':fit})
    assert out[1]['loaded_bars_before_START']>out[0]['loaded_bars_before_START']
    (ROOT/'C_historial.json').write_text(json.dumps({'START_UTC':'18:54:00','END_UTC':'19:20:00','cases':out},indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in c.items() if k!='extraction'} for c in out],indent=2))
if __name__=='__main__':main()
