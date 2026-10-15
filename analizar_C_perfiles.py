"""Controles de perfil por recurrencia y coincidencia exacta de plots cerrados."""
import json
from pathlib import Path
from obtener_C import recover
from comparar_resolucion_C import compare
ROOT=Path(__file__).parent
def main():
    reference='C_referencia_restaurada_limites.csv'
    result={}
    for profile in ('A','C','D'):
        name=f'C_perfil_{profile}_fuente1m.csv'
        fit=recover(ROOT/name)
        comparison=next(x for x in compare(reference,name) if x['phase_seconds']==0 and x['reference_shift_seconds']==0)
        assert fit['compatible_integer_C_seconds']==[62]
        assert comparison['max_error']==0
        fit['scope']='Control empirico de este rango; no implica invariancia de todas las señales o modos.'
        result[profile]={'fit':fit,'comparison':comparison}
    (ROOT/'C_control_perfiles.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({p:{'C':v['fit']['compatible_integer_C_seconds'],
        'matching_values':v['comparison']['values'],'max_error':v['comparison']['max_error']}
        for p,v in result.items()},indent=2))
if __name__=='__main__':main()
