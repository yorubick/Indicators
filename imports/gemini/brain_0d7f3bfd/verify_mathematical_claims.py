import json
from pathlib import Path
import pandas as pd
import numpy as np

# Load the master 112 cases
cases_path = Path('C:/Users/PC/.gemini/antigravity/brain/0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27/scratch/cases_112.json')
cases = json.loads(cases_path.read_text())

print(f"Total verified cases loaded: {len(cases)}\n")

# ==============================================================================
# PROOF 1: SHORT RULE (n < 21)
# Formula: C = max(dt, round(n * dt * 10 / 183))
# ==============================================================================
print("=" * 70)
print("PRUEBA 1: VERIFICACIÓN DEL RÉGIMEN CORTO (n < 21 velas)")
print("=" * 70)
short_cases = [c for c in cases if c['bars'] < 21]
short_results = []
for c in short_cases:
    n = c['bars']
    dt = c['dt']
    actual = c['C']
    formula_c = max(float(dt), n * dt * 10.0 / 183.0)
    err = abs(formula_c - actual)
    short_results.append({
        'id': c['id'],
        'n': n,
        'dt': dt,
        'actual_C': round(actual, 2),
        'formula_C': round(formula_c, 2),
        'diff': round(err, 4),
        'match': err < 0.5
    })

df_short = pd.DataFrame(short_results)
print(df_short.to_string(index=False))
print(f"\nAciertos en Régimen Corto: {df_short['match'].sum()} / {len(df_short)} ({df_short['match'].sum()/len(df_short)*100:.1f}%)")
print(f"Error medio absoluto (MAE): {df_short['diff'].mean():.4f} segundos\n")

# ==============================================================================
# PROOF 2: CONSOLIDATION RULE M=24 (1m chart, compressed ranges)
# Formula: C = floor(t_span / 24) = floor((n - 1) * 60 / 24)
# ==============================================================================
print("=" * 70)
print("PRUEBA 2: VERIFICACIÓN DEL RÉGIMEN DE CONSOLIDACIÓN M=24 (1 minuto)")
print("=" * 70)
# Look at 1m cases with consolidation (e.g. 18:55 to 19:20, duration 25 min)
# Let's inspect all 1m cases in cases_112 where rng <= 24
m24_cases = []
for c in cases:
    if c['dt'] == 60 and c['bars'] >= 21:
        highs = [x['high'] for x in c['OHLC']]
        lows = [x['low'] for x in c['OHLC']]
        rng = max(highs) - min(lows)
        t_span = (c['bars'] - 1) * 60
        pred_m24 = int(np.floor(t_span / 24.0))
        m24_cases.append({
            'id': c['id'],
            'START': c['START'].split('T')[1][:5],
            'END': c['END'].split('T')[1][:5],
            'n': c['bars'],
            'rng_pts': round(rng, 2),
            'actual_C': round(c['C'], 1),
            'formula_M24': pred_m24,
            'diff': round(abs(pred_m24 - c['C']), 1)
        })

df_m24 = pd.DataFrame(m24_cases)
# Focus on compressed ranges rng <= 25
compressed = df_m24[df_m24['rng_pts'] <= 25.0]
print(compressed.head(15).to_string(index=False))

# ==============================================================================
# PROOF 3: 15-SECOND EXPERIMENTAL AUDIT (Codex Challenge: 13 controls)
# ==============================================================================
print("\n" + "=" * 70)
print("PRUEBA 3: AUDITORÍA EN 15 SEGUNDOS (Los 13 controles del desafío de Codex)")
print("=" * 70)
import evaluate_unified_model_v4 as model_v4

ctrl_13 = [c for c in cases if c['partition'] == 'additional_controls']
ctrl_results = []
for c in ctrl_13:
    pred, branch = model_v4.predict_C(c)
    actual = c['C']
    err = abs(pred - actual)
    ctrl_results.append({
        'START': c['START'].split('T')[1][:8],
        'END': c['END'].split('T')[1][:8],
        'n': c['bars'],
        'actual_C': round(actual, 1),
        'model_C': round(pred, 1),
        'diff': round(err, 2),
        'branch': branch,
        'exact': err < 0.1
    })

df_ctrl = pd.DataFrame(ctrl_results)
print(df_ctrl.to_string(index=False))
print(f"\nAciertos Exactos en los 13 controles de Codex: {df_ctrl['exact'].sum()} / {len(df_ctrl)} ({df_ctrl['exact'].sum()/len(df_ctrl)*100:.1f}%)")
print(f"Error medio absoluto (MAE): {df_ctrl['diff'].mean():.2f} segundos\n")

# ==============================================================================
# PROOF 4: THE 6 CURVE EQUATIONS (Lite EMA periods check)
# ==============================================================================
print("=" * 70)
print("PRUEBA 4: PRECISIÓN DE LOS PERÍODOS DE LAS 6 CURVAS DE POISZN LITE")
print("=" * 70)
# Check G:/trading/guias/analisis/C_cruce1903_resultados.json
res_cruce = json.loads(Path('G:/trading/guias/analisis/C_cruce1903_resultados.json').read_text())
for case in res_cruce['cases']:
    print(f"Caso {case['id']} (START {case['START'][11:19]}, END {case['END'][11:19]}): C={case['C']:.4f}")
    for lane, data in case['Lite_fits'].items():
        expected_len = (72.0 if 'Fast' in lane or 'A' in lane else 89.0)
        # Check base divisor: Lane 3 divisor 3, Lane 2 divisor 9, Lane 1 divisor 27
        div = 3.0 if '3' in lane else (9.0 if '2' in lane else 27.0)
        mult = 72.0 if 'A' in lane else 89.0
        formula_period = (mult / div) * (case['C'] / 15.0)
        fit_period = data['period']
        rmse = data['rmse']
        print(f"  {lane:9s}: Período Medido = {fit_period:10.5f} | Período Fórmula = {formula_period:10.5f} | Discrepancia = {abs(fit_period - formula_period):.2e} | RMSE = {rmse:.2e}")
