"""Audita una fórmula parcial; no ajusta umbrales ni usa validación."""
import json, math
from pathlib import Path
from lab_base_C import states

ROOT = Path(__file__).parent

def describe(c):
    r = c['OHLC']; h = list(states(r)); a, p = h[-1], h[-2]
    net = r[-1]['close'] - r[0]['close']
    body = r[-1]['close'] - r[-1]['open']
    return {
        'new_high': a['new_high'], 'new_low': a['new_low'],
        'confirmed_high_END': a['last_confirmed_high'] != p['last_confirmed_high'],
        'confirmed_low_END': a['last_confirmed_low'] != p['last_confirmed_low'],
        'global_high_after_low': a['idx_high'] > a['idx_low'],
        'net_up': net > 0, 'END_body_up': body > 0,
        'START_body_up': r[0]['close'] > r[0]['open'],
        'END_body_against_net': net * body < 0,
    }

def main():
    cases = [c for c in json.loads((ROOT/'C_dataset_verificado.json').read_text())['cases']
             if c['split'] == 'training' and c['branch'] == 'long']
    rows = []
    for c in cases:
        span = (c['bars']-1)*c['dt']; predicted = math.floor(span/24)
        rows.append({'id': c['id'], 'START': c['START'], 'END': c['END'],
                     'dt': c['dt'], 'bars': c['bars'], 'span': span,
                     'C': c['C'], 'duration24': predicted,
                     'match': abs(c['C']-predicted) < 1e-7, 'features': describe(c)})
    positives = [r for r in rows if r['match']]
    common = {k: positives[0]['features'][k] for k in positives[0]['features']
              if all(r['features'][k] == positives[0]['features'][k] for r in positives)}
    false_positives = [r['id'] for r in rows if not r['match'] and
                      all(r['features'][k] == v for k,v in common.items())]
    # For floor(span/d)=C>0, divisor interval is (span/(C+1),span/C].
    lower = max(r['span']/(round(r['C'])+1) for r in positives)
    upper = min(r['span']/round(r['C']) for r in positives)
    audit = {}
    for k in common:
        v = common[k]
        audit[k] = {'value': v, 'matches_selected': len(positives),
                    'nonmatches_also_selected': sum(not r['match'] and r['features'][k] == v for r in rows)}
    out = {'scope': 'Training long only. Retrospective audit, no prospective success or classifier fitted.',
           'validation_used': False, 'training_cases': len(rows), 'matches': len(positives),
           'common_predicates': audit, 'conjunction_false_positives': false_positives,
           'divisor_compatible_interval': {'lower_exclusive': lower, 'upper_inclusive': upper},
           'positive_dates': sorted(set(r['START'][:10] for r in positives)),
           'cases': rows}
    (ROOT/'C_rama24_auditoria.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k != 'cases'},indent=2))

if __name__ == '__main__': main()
