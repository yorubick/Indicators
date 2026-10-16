"""Gráfico vectorial de precio y eventos registrados, sin usar C para marcarlos."""
from pathlib import Path
from reportlab.graphics.shapes import Drawing,String,Line,Rect,Circle
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics import renderSVG
from reportlab.lib import colors
from analizar_C_frontera_1s import read
from analizar_C_bordes26 import stamp
import xml.etree.ElementTree as ET

ROOT=Path(__file__).parent
rows=read(ROOT/'manual/C_startSweep1920_geometria_historia_larga.csv')
s,e=stamp('18:35'),stamp('19:35');stamps=list(range(s,e+1,60))
lo=min(float(rows[t]['low']) for t in stamps);hi=max(float(rows[t]['high']) for t in stamps)
d=Drawing(1100,680)
d.add(String(45,651,'12 octubre 2026 UTC - eventos estructurales registrados sobre precio',fontSize=16))
plot=LinePlot();plot.x=70;plot.y=225;plot.width=975;plot.height=355
plot.data=[[(i,float(rows[t]['close'])) for i,t in enumerate(stamps)]]
plot.xValueAxis.valueMin=0;plot.xValueAxis.valueMax=60;plot.xValueAxis.valueSteps=list(range(0,61,10))
plot.yValueAxis.valueMin=lo-2;plot.yValueAxis.valueMax=hi+2
plot.lines[0].strokeColor=colors.HexColor('#334155');plot.lines[0].strokeWidth=1.5
d.add(plot)
def X(time):return 70+(stamp(time)-s)/60/60*975
def Y(price):return 225+(price-(lo-2))/(hi-lo+4)*355
events=[('18:45','High previo',30886.5),('18:52','Origen low',30844.25),('18:54','High recuperacion',30861.5),
        ('19:05','Close rompe high',30863),('19:07','Primer pivot',30857.75),('19:10','Retroceso profundo',30849),('19:17','Ultimo pivot',30851.5)]
for i,(time,label,p) in enumerate(events):
    d.add(Line(X(time),225,X(time),580,strokeColor=colors.HexColor('#cbd5e1'),strokeDashArray=[3,4]))
    d.add(Circle(X(time),Y(p),3,fillColor=colors.HexColor('#be123c'),strokeColor=None))
    d.add(String(X(time)+4,Y(p)+5,str(i+1),fontSize=9))
    d.add(String(70+(i%3)*320,625-(i//3)*17,f'{i+1}: {time} - {label}',fontSize=9))
d.add(String(70,207,'x: minutos desde18:35. Linea=close; puntos=high/low/close del evento. No son señales del indicador.',fontSize=10))
boxes=[('B: stall provisional','18:47','18:52','#b45309'),('A: primer pivot','18:52','19:07','#0284c7'),
       ('A: mas profundo','18:52','19:10','#7c3aed'),('A: ultimo pivot','18:52','19:17','#059669')]
for i,(label,a,b,color) in enumerate(boxes):
    y=155-29*i
    d.add(String(70,y+3,label,fontSize=9))
    d.add(Rect(X(a),y,X(b)-X(a),12,fillColor=colors.HexColor(color),strokeColor=None))
    d.add(String(X(b)+8,y+2,a+'-'+b,fontSize=9))
d.add(String(70,28,'Pivots1vela confirmada; interpretacion operativa provisional. Anclas congeladas antes de las nuevas mediciones C.',fontSize=10))
path=ROOT/'media/C_estructura_eventos.svg';renderSVG.drawToFile(d,str(path));ET.parse(path)
print(path)
