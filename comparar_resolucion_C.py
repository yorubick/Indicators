"""Compara los plots por timestamp; no supone que las series 15s sean EMA 15s."""
import csv,json
from pathlib import Path
from identificar_emas import COLUMNS
ROOT=Path(__file__).parent
def read(name):
    with (ROOT/name).open(encoding='utf-8-sig',newline='') as f:
        return {int(r['time']):r for r in csv.DictReader(f)}
def compare(reference,other):
    a,b=read(reference),read(other)
    output=[]
    # Ambos archivos pueden contener una ultima vela en curso de distinto momento.
    cutoff=min(max(a),max(b))-120
    for phase in (0,15,30,45):
        for shift in (-60,0,60):
            errors=[];times=set()
            for t,r in b.items():
                if t%60!=phase or t>=cutoff:continue
                q=a.get(t-phase+shift)
                if not q:continue
                for k in COLUMNS:
                    if r.get(k) and q.get(k):
                        errors.append(abs(float(r[k])-float(q[k])));times.add(t)
            if errors:output.append(dict(phase_seconds=phase,reference_shift_seconds=shift,
                minute_samples=len(times),values=len(errors),closed_before=cutoff,max_error=max(errors),
                mean_error=sum(errors)/len(errors)))
    return sorted(output,key=lambda x:x['max_error'])
if __name__=='__main__':
    result=compare('C_referencia_restaurada_limites.csv','C_fuente1m_grafico15s.csv')
    (ROOT/'C_control_resolucion.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result[:4],indent=2))
