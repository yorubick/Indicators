import csv,json
from pathlib import Path
from obtener_C import recover
from comparar_resolucion_C import compare,read
from identificar_emas import COLUMNS
ROOT=Path(__file__).parent
def main():
    reverse=read('C_anclas_invertidas_25m.csv')
    populated=sum(bool(r.get(k)) for r in reverse.values() for k in COLUMNS)
    assert populated==0
    result={'reversed_anchors':{'file':'C_anclas_invertidas_25m.csv',
        'curve_values':populated,'interpretation':'No hay curvas; no se asigna C cero.'},'directions':{}}
    reference='C_referencia_restaurada_perfiles.csv'
    for direction in ('Bull','Bear'):
        file=f'C_flow_{direction}_25m.csv'
        fit=recover(ROOT/file)
        comparison=next(x for x in compare(reference,file) if x['phase_seconds']==0 and x['reference_shift_seconds']==0)
        assert fit['compatible_integer_C_seconds']==[62] and comparison['max_error']==0
        fit['scope']='Direccion de Flow Bands; no es Setup direction del modo Auto Balanced.'
        a,b=read(reference),read(file)
        changes={}
        for key in ('Bull delivery active','Bear delivery active'):
            pairs=[(a[t].get(key),b[t].get(key)) for t in a.keys() & b.keys() if t<comparison['closed_before']]
            changes[key]={'timestamps_compared':len(pairs),'different_values':sum(x!=y for x,y in pairs)}
        result['directions'][direction]={'fit':fit,'curve_comparison':comparison,'active_signals':changes}
    (ROOT/'C_orden_direccion.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({d:{'C':r['fit']['compatible_integer_C_seconds'],'matching_values':r['curve_comparison']['values'],
        'signal_changes':r['active_signals']} for d,r in result['directions'].items()},indent=2))
if __name__=='__main__':main()
