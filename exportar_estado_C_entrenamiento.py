"""Construye estados ex-ante, solo entrenamiento, para candidatos estructurales."""
import json
from pathlib import Path
from lab_base_C import states,estimate_C,experimental_consolidation
ROOT=Path(__file__).parent
def main():
    d=json.loads((ROOT/'C_dataset_verificado.json').read_text());out=[]
    for case in d['cases']:
        if case['split']!='training':continue
        history=list(states(case['OHLC']));final=history[-1]
        out.append({'id':case['id'],'START':case['START'],'END':case['END'],'dt':case['dt'],'C_original_for_scoring_only':case['C'],'estimate':estimate_C(final,case['dt']),'consolidation_hypothesis':experimental_consolidation(final,case['dt']),'final_state':final,'state_history':history})
    result={'scope':'Observable candidate state, not original hidden state. Numeric labels kept separate from causal state construction. Only53training cases exported; validation not processed.','cases':out}
    (ROOT/'C_estado_entrenamiento.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'cases':len(out),'long_cases_with_C_none':sum(c['estimate']['C']is None for c in out),'short_rule_matches':sum(c['estimate']['C']is not None and abs(c['estimate']['C']-c['C_original_for_scoring_only'])<1e-7 for c in out)},indent=2))
if __name__=='__main__':main()
