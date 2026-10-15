"""Recupera un intervalo de C de los plots originales exportados.
No deduce C exclusivamente del OHLC ni accede a codigo privado.
Uso: python obtener_C.py archivo.csv
Requiere que fuente y grafico tengan la misma resolucion.
"""
import csv,json,math,statistics,sys
from pathlib import Path
from identificar_emas import analyze
BASE={'Layer A':72/3,'Layer A boundary':89/3,
      'Layer B':72/9,'Layer B boundary':89/9,
      'Layer C':72/27,'Layer C boundary':89/27,
      'Extra cloud 1':72,'Extra cloud 1 boundary':89,
      'Extra cloud 2':216,'Extra cloud 2 boundary':267}

def recover(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    differences=[int(b['time'])-int(a['time'])for a,b in zip(rows,rows[1:])
                 if int(b['time'])>int(a['time'])]
    if not differences:raise ValueError('No hay suficientes timestamps')
    dt=statistics.median(differences)
    if dt!=int(dt):raise ValueError('Intervalo fuente no regular')
    fit=analyze(path,int(dt))
    periods={}
    for k,v in fit['layers'].items():
        if v.get('available') is False or v.get('pairs',0)<5:
            raise ValueError(f'{k}: faltan muestras consecutivas de curvas')
        if v['source']!='close' or v['rmse_step']>1e-8 or abs(v['period']-round(v['period']))>1e-6:
            raise ValueError(f'{k}: no coincide con EMA de cierre de periodo entero. Verifica fuente y grafico.')
        periods[k]=round(v['period'])
    lower=max((periods[k]-.5)*dt/base for k,base in BASE.items())
    upper=min((periods[k]+.5)*dt/base for k,base in BASE.items())
    if lower>=upper:raise ValueError('Los plots no siguen la familia 72/89 comprobada')
    integers=[c for c in range(math.ceil(lower),math.ceil(upper))if lower<=c<upper]
    return {'file':str(path.resolve()),'source_seconds':int(dt),
            'C_seconds_interval':{'lower_inclusive':lower,'upper_exclusive':upper},
            'compatible_integer_C_seconds':integers,
            'periods':periods,'pairs_per_curve':min(v['pairs']for v in fit['layers'].values()),
            'max_rmse_step':max(v['rmse_step']for v in fit['layers'].values()),
            'scope':'C inferido de plots originales; no generado solo desde OHLC. Perfil B probado.'}

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Uso: python obtener_C.py archivo.csv')
    try:result=recover(Path(sys.argv[1]))
    except (ValueError,KeyError,StopIteration) as error:raise SystemExit(str(error))
    print(json.dumps(result,indent=2,ensure_ascii=False))
