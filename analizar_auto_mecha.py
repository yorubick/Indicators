"""Compara curvas ante cambios del precio ancla sin atribuir C no validado."""
import csv,json,math
from pathlib import Path
from datetime import datetime
from identificar_emas import COLUMNS,analyze
ROOT=Path(__file__).parent
def stamp(s):return int(datetime.fromisoformat('2026-10-12T'+s+'+00:00').timestamp())
def read(name):
    with (ROOT/name).open(encoding='utf-8-sig') as f:return {int(r['time']):r for r in csv.DictReader(f)}
def compare(a_name,b_name):
    a,b=read(a_name),read(b_name)
    common=sorted(t for t in a.keys() & b.keys() if stamp('19:40:00')<=t<stamp('20:40:00'))
    assert common
    assert all(a[t][k]==b[t][k] for t in common for k in ('open','high','low','close'))
    output={}
    for k in COLUMNS:
        pairs=[(float(a[t][k]),float(b[t][k])) for t in common if a[t][k] and b[t][k]]
        assert len(pairs)>5
        differences=[x-y for x,y in pairs]
        output[k]={'values':len(pairs),'different_values':sum(d!=0 for d in differences),
            'max_absolute_difference':max(map(abs,differences)),
            'rmse_difference':math.sqrt(sum(d*d for d in differences)/len(differences))}
    return {'timestamps_with_same_OHLC':len(common),'curves':output}
def main():
    result={'mode':'Auto Balanced','END_UTC':'19:20:00','wick_time_UTC':'19:30:00',
        'setup_direction':'Bullish','chart_seconds':5,'price_control':'30871 real low; 30872/30873 synthetic input prices',
        'comparisons':{},'C_scope':'C no asignado: recurrencia de cierres del grafico no validada en Auto.'}
    for price in (30872,30873):
        result['comparisons'][str(price)]=compare('C_auto_END1920_wick1930_30871_5s.csv',f'C_auto_END1920_wick1930_{price}_5s.csv')
    result['wick_time_controls']={}
    for minute in (31,32):
        result['wick_time_controls'][f'19:{minute}']=compare('C_auto_END1920_wick1930_30871_5s.csv',f'C_auto_END1920_wick19{minute}_precio30871_5s.csv')
    result['manual_control']=compare('C_manual_1920_1930_precio30871.csv','C_manual_1920_1930_precio30873.csv')
    from obtener_C import recover
    result['manual_extractions']=[recover(ROOT/f'C_manual_1920_1930_precio{price}.csv') for price in (30871,30873)]
    assert all(v['different_values']==0 for v in result['manual_control']['curves'].values())
    assert result['manual_extractions'][0]['periods']==result['manual_extractions'][1]['periods']
    (ROOT/'C_auto_mecha.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'auto_changes':{p:{k:v['max_absolute_difference'] for k,v in r['curves'].items()} for p,r in result['comparisons'].items()},
        'manual_C':[r['compatible_integer_C_seconds'] for r in result['manual_extractions']],
        'time_changes':{t:r['curves']['Extra cloud 1'] for t,r in result['wick_time_controls'].items()}},indent=2))
if __name__=='__main__':main()
