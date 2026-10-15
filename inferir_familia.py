"""Contrasta si diez periodos enteros pueden venir de una sola escala C."""
import json,math
from pathlib import Path
ROOT=Path(__file__).parent
BASE={'Layer A':72/3,'Layer A boundary':89/3,
      'Layer B':72/9,'Layer B boundary':89/9,
      'Layer C':72/27,'Layer C boundary':89/27,
      'Extra cloud 1':72,'Extra cloud 1 boundary':89,
      'Extra cloud 2':72*3,'Extra cloud 2 boundary':89*3}
data=json.loads((ROOT/'estudio_rangos.json').read_text(encoding='utf-8'))
out=[]
for case in data:
    observed={k:round(v['period'])for k,v in case['layers'].items()}
    lower=max((observed[k]-.5)/base for k,base in BASE.items())
    upper=min((observed[k]+.5)/base for k,base in BASE.items())
    scalar=(lower+upper)/2
    dt=case.get('step_seconds',60)
    possible_integer_seconds=[c for c in range(math.ceil(lower*dt),math.ceil(upper*dt))
                              if lower<=c/dt<upper]
    if len(possible_integer_seconds)==1:
        scalar=possible_integer_seconds[0]/dt
    predicted={k:math.floor(base*scalar+.5)for k,base in BASE.items()}
    record={'file':case['file'],'start':case['start'],'end':case['end'],
            'C_over_source_interval':{'lower_inclusive':lower,'upper_exclusive':upper},
            'source_seconds':dt,
            'C_seconds_interval':[dt*lower,dt*upper],
            'possible_integer_C_seconds':possible_integer_seconds,
            'consistent':lower<upper,'predicted':predicted,'observed':observed,
            'all_ten_match':predicted==observed}
    out.append(record)
    print(case['start'],case['end'],'source',dt,'C seconds',possible_integer_seconds,'match',record['all_ten_match'])
(ROOT/'familia_character.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
