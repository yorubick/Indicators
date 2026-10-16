"""Figura de mediciones; las líneas conectan observaciones, no interpolan C."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).parent
data=json.loads((ROOT/'C_sensibilidad_15s.json').read_text())
fig,axes=plt.subplots(2,1,figsize=(11,7),layout='constrained')
for ax,records,key,title in [
    (axes[0],data['cases'],'START_UTC','Mover START cada 15 s · END fijo a 19:20:00 UTC'),
    (axes[1],data['END_controls'],'END_UTC','Mover END cada minuto · START fijo a 18:55:00 UTC')]:
    values=[r['extraction']['compatible_integer_C_seconds'][0]for r in records]
    ax.plot(range(len(records)),values,'o-',color='#b76a06',linewidth=1.6)
    for i,v in enumerate(values):ax.annotate(str(v),(i,v),xytext=(0,7),textcoords='offset points',ha='center')
    ax.set_xticks(range(len(records)),[r[key][3:] if key=='START_UTC' else r[key][:5]for r in records])
    ax.set_ylim(50,140);ax.set_ylabel('C compatible (segundos)');ax.set_title(title,loc='left',fontsize=12)
    ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
axes[0].set_xlabel('Inicio a las 18:MM:SS UTC')
axes[1].set_xlabel('Final UTC')
fig.suptitle('Character Tree: sensibilidad de C a las anclas',fontsize=16,ha='left',x=.02)
fig.text(.02,-.035,'NQ1! · 12 oct 2026 · Perfil B · Manual · Fuente y gráfico: 15 segundos\n'
         'C se recupera de los plots originales. Su fórmula generadora sigue pendiente.',fontsize=10,color='#444444')
fig.savefig(ROOT/'media/C_sensibilidad_15s.png',dpi=170,bbox_inches='tight')
