"""Ajuste conjunto de armónicos; C nunca selecciona período ni coeficientes."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
SPEC = {
    'source': 'C_matriz_frontera15s_volumen.json, nueve controles conocidos',
    'price': 'close, timestamps nativos consecutivos',
    'models': {'single': [1], 'ternary': [1, 3, 9], 'binary_control': [1, 2, 4]},
    'regression': 'intercepto+tendencia lineal+cos/sin de cada componente h/P; mínimos cuadrados',
    'period_domain_bars': '[18.000001,4*n], común a los tres modelos; resuelve h=9 sin alias de Nyquist',
    'selection': 'mínimo error cuadrático de precio; fases/amplitudes libres estimadas solo del precio',
    'search': 'mallas logarítmicas721/2161, refinar todos los mínimos locales con60pasos golden-section; extremos incluidos',
    'C_mapping': 'C=K*dt*P, K positivo común; permitir C observado +/-1 segundo para cubrir redondeos',
    'scope': 'Exploratorio, etiquetas ya conocidas, no validación independiente. No nueva medición TradingView. Rechaza solo este estimador y esta conversión, no todos los armónicos.',
}


def fit_period(prices, harmonics, grid_size):
    """Esta función recibe precios, sin C ni identidad del caso."""
    y = np.asarray(prices, dtype=float)
    y = (y-y.mean())/np.std(y)
    t = np.arange(len(y), dtype=float)
    trend = (t-t.mean())/len(y)

    def score(period):
        columns = [np.ones(len(y)), trend]
        for harmonic in harmonics:
            angle = 2*np.pi*harmonic*t/period
            columns.extend([np.cos(angle), np.sin(angle)])
        design = np.column_stack(columns)
        coefficients, _, rank, _ = np.linalg.lstsq(design, y, rcond=None)
        if rank != len(columns):
            return float('inf')
        return float(np.sum((y-design@coefficients)**2))

    grid = np.geomspace(18.000001, 4*len(y), grid_size)
    errors = [score(p) for p in grid]
    candidates = [(errors[0], float(grid[0])), (errors[-1], float(grid[-1]))]
    ratio = float((np.sqrt(5)-1)/2)
    for i in range(1, len(grid)-1):
        if errors[i] > errors[i-1] or errors[i] > errors[i+1]:
            continue
        low, high = float(grid[i-1]), float(grid[i+1])
        left, right = high-ratio*(high-low), low+ratio*(high-low)
        left_error, right_error = score(left), score(right)
        for _ in range(60):
            if left_error <= right_error:
                high, right, right_error = right, left, left_error
                left = high-ratio*(high-low)
                left_error = score(left)
            else:
                low, left, left_error = left, right, right_error
                right = low+ratio*(high-low)
                right_error = score(right)
        period = (low+high)/2
        candidates.append((score(period), period))
    error, period = min(candidates)
    return {'period_bars': period, 'normalized_RSS': error, 'grid_size': grid_size,
            'refined_local_minima': len(candidates)-2,
            'at_upper_boundary': abs(period-4*len(y)) < 1e-6,
            'at_lower_boundary': abs(period-18.000001) < 1e-6}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec', action='store_true')
    args = parser.parse_args()
    spec_path = ROOT/'C_armonicos_conjuntos_preregistro.json'
    if args.spec:
        spec_path.write_text(json.dumps(SPEC, indent=2, ensure_ascii=False), encoding='utf-8')
        print('Reglas congeladas antes de evaluar.')
        return
    assert json.loads(spec_path.read_text(encoding='utf-8')) == SPEC
    dataset_path = ROOT/SPEC['source'].split(',')[0]
    cases = json.loads(dataset_path.read_text(encoding='utf-8'))['cases']
    assert len(cases) == 9
    for case in cases:
        times = [r['time'] for r in case['OHLC']]
        assert len(times) == case['bars']
        assert all(b-a == case['dt'] for a,b in zip(times,times[1:]))
    results = []
    for name, harmonics in SPEC['models'].items():
        records = []
        for case in cases:
            prices = [r['close'] for r in case['OHLC']]
            coarse = fit_period(prices, harmonics, 721)
            dense = fit_period(prices, harmonics, 2161)
            scale = case['dt']*dense['period_bars']
            records.append({k:case[k] for k in ['START','END','bars','dt','C']} |
                {'coarse':coarse, 'dense':dense,
                 'period_relative_change': abs(coarse['period_bars']/dense['period_bars']-1),
                 'K_interval':[(case['C']-1)/scale,(case['C']+1)/scale]})
        lo = max(r['K_interval'][0] for r in records)
        hi = min(r['K_interval'][1] for r in records)
        lower = max(records,key=lambda r:r['K_interval'][0])
        upper = min(records,key=lambda r:r['K_interval'][1])
        results.append({'model':name,'harmonics':harmonics,'common_K_interval':[lo,hi],
            'common_K_exists':lo<=hi,
            'max_period_relative_change':max(r['period_relative_change'] for r in records),
            'lower_witness':{k:lower[k] for k in ['START','END','C','K_interval']},
            'upper_witness':{k:upper[k] for k in ['START','END','C','K_interval']},
            'cases':records})
    # Extensión posterior al primer resultado: permitir cualquier componente por caso.
    # Es una condición necesaria generosa; no utiliza C para volver a estimar P.
    ternary = next(r for r in results if r['model']=='ternary')
    feasible = [(0.0, float('inf'))]
    component_cases = []
    for case in ternary['cases']:
        options = [(h*case['K_interval'][0],h*case['K_interval'][1]) for h in [1,3,9]]
        feasible = [(max(a,c),min(b,d)) for a,b in feasible for c,d in options if max(a,c)<=min(b,d)]
        component_cases.append({k:case[k] for k in ['START','END','C']} |
                               {'K_interval_options_for_h1_h3_h9':options})
    component_test = {'timing':'Supplementary after the first result; exploratory, not original preregistration',
        'hypothesis':'C=K*dt*P/h, allow h1/3/9 independently per case with no selection rule required',
        'common_K_union':feasible,'necessary_condition_passes':bool(feasible),'cases':component_cases}
    # Comprobación del estimador: un ciclo sintético conocido y transformación afín.
    t = np.arange(90)
    synthetic = 0.03*t+np.sin(2*np.pi*t/36)+0.7*np.cos(2*np.pi*3*t/36)+0.2*np.sin(2*np.pi*9*t/36)
    fitted = fit_period(synthetic, [1,3,9], 721)
    transformed = fit_period(10000+2*synthetic, [1,3,9], 721)
    assert abs(fitted['period_bars']-36) < 1e-5
    assert abs(transformed['period_bars']-fitted['period_bars']) < 1e-5
    out = {'spec':SPEC,'dataset_SHA256':hashlib.sha256(dataset_path.read_bytes()).hexdigest(),
        'results':results,'synthetic_estimator_check':{'known_period':36,'fit':fitted,'affine_fit':transformed},
        'supplementary_component_selection':component_test,
        'warning':'Lower RSS of the ternary model does not prove ternary price cycles: it has more coefficients than the single model.'}
    (ROOT/'C_armonicos_conjuntos_resultados.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps([{k:v for k,v in r.items() if k!='cases'} for r in results],indent=2))
    print('Prueba sintética del estimador y transformación afín: correctas.')
    print('Selección libre de componente1/3/9, K común factible:',bool(feasible))


if __name__ == '__main__':
    main()
