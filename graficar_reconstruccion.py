"""Figura independiente: original exportado, reconstruccion y error acumulado."""
import csv
from datetime import datetime, timezone
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ROOT = Path(__file__).parent
with (ROOT/'character_manual_15m_1m.csv').open(encoding='utf-8-sig',newline='') as f:
    rows = list(csv.DictReader(f))[:-1]
anchor = 1791781200
seed = float(next(r for r in rows if int(r['time']) == anchor)['high'])
periods = {'Layer A':24,'Layer A boundary':30,'Layer B':8,'Layer B boundary':10,
           'Layer C':3,'Layer C boundary':3,'Extra cloud 1':72,
           'Extra cloud 1 boundary':89,'Extra cloud 2':216,'Extra cloud 2 boundary':267}
state = dict.fromkeys(periods,seed)
times,prices = [],[]
original = {k:[] for k in periods}
replica = {k:[] for k in periods}
for r in rows:
    if int(r['time']) <= anchor:
        continue
    times.append(datetime.fromtimestamp(int(r['time']),timezone.utc))
    prices.append(float(r['close']))
    for k,n in periods.items():
        state[k] += 2/(n+1)*(float(r['close'])-state[k])
        original[k].append(float(r[k]))
        replica[k].append(state[k])
fig,(ax,err)=plt.subplots(2,1,figsize=(12,7),sharex=True,
                          gridspec_kw={'height_ratios':[4,1]},layout='constrained')
colors=['#d77700','#d77700','#edae37','#edae37','#ffd170','#ffd170',
        '#5693b4','#5693b4','#9774b5','#9774b5']
ax.plot(times,prices,color='#777777',lw=.65,label='Cierre NQ1!')
for (k,n),color in zip(periods.items(),colors):
    ax.plot(times,original[k],color=color,lw=1.6,alpha=.75)
    ax.plot(times,replica[k],color='black',lw=.45,ls='--')
    err.plot(times,[a-b for a,b in zip(replica[k],original[k])],color=color,lw=.8)
ax.plot([],[],color='#d77700',label='Curvas del indicador (CSV)')
ax.plot([],[],color='black',ls='--',lw=.8,label='Reconstrucción EMA independiente')
ax.legend(loc='upper right',fontsize=9)
ax.set_title('Character Tree: diez curvas reconstruidas en 877 velas de 1 minuto',fontsize=14)
ax.set_ylabel('Precio (puntos)')
err.set_ylabel('Error\n(puntos)')
err.set_xlabel('12 octubre 2026 · UTC')
err.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M',tz=timezone.utc))
for axis in [ax,err]:
    axis.grid(alpha=.2)
fig.savefig(ROOT/'reconstruccion_character.png',dpi=160)
print('Figura guardada. Error máximo:',max(abs(a-b) for k in periods for a,b in zip(replica[k],original[k])))
