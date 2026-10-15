"""Repite62/83, audita datos y genera comparación numérica y SVG con ReportLab."""
import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
from analizar_C_frontera_1s import read
from analizar_C_fuente_vs_grafico import fit_lite,LANES
from analizar_C_traslacion50 import comparison
from medir_C_geometria_ema import PERIODS,ema_series
from reportlab.graphics.shapes import Drawing,String
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.lib import colors
from reportlab.graphics import renderSVG

ROOT=Path(__file__).parent

def ts(t):return int(datetime.fromisoformat('2026-10-12T'+t+':00+00:00').timestamp())

def main():
    source=read(ROOT/'manual/C_startSweep1920_geometria_historia_larga.csv')
    old=json.loads((ROOT/'C_geometria_controles_resultados.json').read_text())['results']
    output={};data={};hashes={}
    for suffix,expected in [('1421',62),('1422',83)]:
        paths=[ROOT/'manual'/f'C_visual1400_{suffix}_{k}.csv' for k in ['a','b']]
        a,b=[read(p) for p in paths];data[suffix]=b
        common=set(source)&set(b)
        assert all(source[t][k]==b[t][k] for t in common for k in ['open','high','low','close','Volume'])
        s,e=ts('14:00'),ts('14:'+suffix[-2:])
        assert all(t in b for t in range(s,e+3660,60))
        fits=fit_lite(b,60,60)
        assert all(abs(v['C']-expected)<1e-6 and v['rmse']<1e-8 for v in fits.values())
        hi=max(float(b[t]['high']) for t in range(s,e+1,60));lo=min(float(b[t]['low']) for t in range(s,e+1,60))
        rupture=next(t for t in range(e+60,e+3660,60) if float(b[t]['close'])>hi or float(b[t]['close'])<lo)
        previous=next(r for r in old if r['id']==f'20261012_140000_{suffix}00_60s')
        assert abs(previous['C']-expected)<1e-6
        output[suffix]={'C':expected,'n':(e-s)//60+1,'H':hi,'L':lo,'rupture':datetime.fromtimestamp(rupture,timezone.utc).isoformat(),
                        'fits':fits,'repeat':comparison(a,b),'native_common_bars':len(common),
                        'geometry':previous['geometry'],'EMA_endpoint_distances':[{'period':m['period'],'START':m['START']['distance'],'END':m['END']['distance']} for m in previous['EMA']],
                        'signature8':previous['signatures']['8']}
        hashes.update({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    assert output['1421']['signature8']==output['1422']['signature8']
    ret=read(ROOT/'manual/C_visual1400_regreso.csv')
    back=comparison(read(ROOT/'manual/C_simetria1855_base.csv'),ret)
    assert all(abs(v['C']-62)<1e-6 for v in fit_lite(ret,60,60).values())
    result={'cases':output,'same_eight_EMA_discrete_signature':True,'return_check':back,'sha256':hashes,
            'scope':'Known pair repeated in Litev1.2; different count, endpoint OHLC and continuous geometry. Output curve difference is not evidence of upstream harmonic cause.'}
    (ROOT/'C_visual1400_resultados.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    # Standard ReportLab chart library; separate fixed reference EMAs from actual Lite outputs.
    drawing=Drawing(1100,650)
    drawing.add(String(35,625,'12 oct 2026 UTC: referencia historica frente a salida Lite',fontSize=16))
    palette=[colors.HexColor(x) for x in ['#111827','#b45309','#7c3aed','#059669','#0891b2','#db2777','#4f46e5']]
    H=output['1421']['H'];L=output['1421']['L'];R=H-L
    primary={N:ema_series(source,N,0) for N in PERIODS[:6]}
    chart=LinePlot();chart.x=60;chart.y=360;chart.width=980;chart.height=210
    stamps=list(range(ts('14:00'),ts('14:22')+1,60))
    chart.data=[[(i,(float(source[t]['close'])-L)/R) for i,t in enumerate(stamps)]]+[
        [(i,(primary[N][t]-L)/R) for i,t in enumerate(stamps)] for N in PERIODS[:6]]
    chart.xValueAxis.valueMin=0;chart.xValueAxis.valueMax=22;chart.xValueAxis.valueSteps=[0,5,10,15,20,22]
    for i in range(7):chart.lines[i].strokeColor=palette[i];chart.lines[i].strokeWidth=2 if i==0 else 1
    drawing.add(chart);drawing.add(String(60,590,'A: close y seis EMAs FIJAS de referencia; x=minutos desde14:00; y=(P-L)/(H-L)',fontSize=11))
    drawing.add(String(60,338,'Negro=close; colores=periodos24,29.667,8,9.889,2.667,3.296. No son longitudes internas demostradas.',fontSize=10))
    chart2=LinePlot();chart2.x=60;chart2.y=90;chart2.width=980;chart2.height=200
    chart2.data=[]
    for suffix in ['1421','1422']:
        for lane in ['Lane 3 A','Lane 2 A','Lane 1 A']:
            chart2.data.append([((t-ts('14:00'))/60,(float(data[suffix][t][lane])-L)/R) for t in range(ts('14:23'),ts('14:45')+1,60) if data[suffix][t][lane]])
    chart2.xValueAxis.valueMin=23;chart2.xValueAxis.valueMax=45;chart2.xValueAxis.valueSteps=[23,25,30,35,40,45]
    for i in range(6):
        chart2.lines[i].strokeColor=palette[1+i%3];chart2.lines[i].strokeWidth=2
        if i>=3:chart2.lines[i].strokeDashArray=[4,3]
    drawing.add(chart2);drawing.add(String(60,310,'B: salidas Lite REALES A de las tres capas; continuo=C62, discontinuo=C83; misma escala H/L',fontSize=11))
    drawing.add(String(60,55,'La firma discreta de8EMAs coincide; las distancias y geometria no. C62/83 confirmado por6recurrencias.',fontSize=11))
    renderSVG.drawToFile(drawing,str(ROOT/'C_comparacion1400_normalizada.svg'))
    print(json.dumps({'summary':{k:{n:v[n] for n in ['C','n','H','L','rupture']} for k,v in output.items()},'same_signature8':True,'return_verified':True},indent=2))

if __name__=='__main__':main()
