"""Contrasta la fórmula propuesta explícitamente por el usuario/Gemini."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).parent
OFFSETS = [-27, -18, -9, 0, 9, 18, 27]
cases = json.loads((ROOT/'C_matriz_frontera15s_volumen.json').read_text(encoding='utf-8'))['cases']
results = []
for case in cases:
    value = case['bars']*case['dt']/18.3
    assert abs((value-math.floor(value))-.5) > 1e-8, 'round tie needs explicit convention'
    base = math.floor(value+.5)
    candidates = [base+offset for offset in OFFSETS]
    nearest = min(candidates, key=lambda c:abs(c-case['C']))
    results.append({k:case[k] for k in ['START','END','dt','bars','C']} |
                   {'base':base, 'required_offset':case['C']-base,
                    'nearest_candidate':nearest,'absolute_error':abs(nearest-case['C']),
                    'matches':abs(nearest-case['C'])<1e-7,
                    'within_one_second':abs(nearest-case['C'])<=1+1e-7})
out = {'hypothesis':'C=round(n*dt/18.3)+offset, offset in [-27,-18,-9,0,9,18,27]',
       'scope':'Known nine controls, arbitrary offset selection allowed separately per case. No selector needed for this necessary test; no new measurements.',
       'exact_matches':sum(c['matches'] for c in results),
       'within_one_second':sum(c['within_one_second'] for c in results),'cases':results}
(ROOT/'C_gemini_offset9_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
