import csv,json
from pathlib import Path
from datetime import datetime
from familia_ema import periodos
ROOT=Path(__file__).parent
cases=json.loads((ROOT/'familia_character.json').read_text(encoding='utf-8'))
details=json.loads((ROOT/'estudio_rangos.json').read_text(encoding='utf-8'))
results=[]
for case,detail in zip(cases,details):
    c=case['possible_integer_C_seconds']
    if len(c)!=1:raise ValueError('C no identificado como entero unico')
    periods=periodos(c[0],case['source_seconds'])
    assert periods==case['observed'],(case['file'],periods,case['observed'])
    result={'file':case['file'],'C_seconds':c[0],'source_seconds':case['source_seconds'],
            'all_periods_match':True}
    if detail['anchor_ohlc']:
        inferred=[v['seed_at_end_if_all_closes_processed']for v in detail['layers'].values()]
        seed=sum(inferred)/len(inferred)
        side=min(['high','low'],key=lambda k:abs(detail['anchor_ohlc'][k]-seed))
        seed=detail['anchor_ohlc'][side]
        end=int(datetime.fromisoformat('2026-10-12T'+detail['end']+':00+00:00').timestamp())
        rows=list(csv.DictReader(Path(case['file']).open(encoding='utf-8-sig')))[:-1]
        state=dict.fromkeys(periods,seed); errors=[]
        for r in rows:
            if int(r['time'])<=end:continue
            for k,n in periods.items():
                state[k]+=2/(n+1)*(float(r['close'])-state[k])
                if r[k]:errors.append(state[k]-float(r[k]))
        result.update(seed_side=side,seed=seed,values_compared=len(errors),
                      max_error=max(map(abs,errors)))
    results.append(result)
(ROOT/'validacion_familia.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('100 periodos coinciden. Reconstrucciones:',[(Path(r['file']).name,r.get('values_compared'),r.get('max_error'))for r in results if 'values_compared'in r])
