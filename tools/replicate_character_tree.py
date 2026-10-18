"""
Herramienta de Verificación y Réplica Exacta de Character Tree v6.5.61
Compara la simulación analítica contra los plots de TradingView extraídos vía CDP.
"""

import json
import numpy as np

def run_replication():
    # 1. Cargar las 300 barras OHLCV
    with open('scratch/bars_ohlcv_300.json') as f:
        bars = json.load(f)

    # 2. Cargar los plots reales de Character Tree
    with open('scratch/all_ct_primitives.json') as f:
        primitives = json.load(f)

    # Buscar el índice de inicio de los plots en CT
    # Sabemos por find_ct_cloud_start que en la configuración actual START=16:40 / END=17:00,
    # los plots empiezan en la vela END (17:00:00 UTC, índice 60)
    time_to_idx = {b['date'][11:16]: b['index'] for b in bars}
    start_box_idx = time_to_idx['16:40']
    end_box_idx = time_to_idx['17:00']

    print(f"Caja: START={bars[start_box_idx]['date']} (idx={start_box_idx}) | END={bars[end_box_idx]['date']} (idx={end_box_idx})")

    # 3. Lookbacks armónicos demostrados para C = 88 s (N_mid = 12)
    # Base 3 recurrence:
    # Slow: u0 = 4, v0 = 5
    # Mid:  u1 = 12, v1 = 15
    # Fast: u2 = 35, v2 = 44
    # Ex1:  u3 = 106, v3 = 131
    # Ex2:  u4 = 317, v4 = 392
    lookbacks = {
        'Fast Center': (35, 1),
        'Fast Boundary': (44, 3),
        'Middle Center': (12, 6),
        'Middle Boundary': (15, 8),
        'Slow Center': (4, 11),
        'Slow Boundary': (5, 13),
        'Extra 1 Center': (106, 16),
        'Extra 1 Boundary': (131, 18),
        'Extra 2 Center': (317, 21),
        'Extra 2 Boundary': (392, 23)
    }

    # Extraer precios de cierre
    closes = np.array([b['close'] for b in bars])
    n_bars = len(closes)

    # Simular las 10 curvas desde la barra 0 de la serie
    simulated_clouds = {}
    for name, (N, plot_col) in lookbacks.items():
        alpha = 2.0 / (N + 1.0)
        ema = np.zeros(n_bars)
        ema[0] = closes[0]
        for t in range(1, n_bars):
            ema[t] = alpha * closes[t] + (1.0 - alpha) * ema[t-1]
        simulated_clouds[name] = ema

    # Cargar valores reales de TradingView en la última barra (idx 299)
    # Obtenidos en tiempo real por inspect_ct_live_plots
    tv_real_last = {
        'Fast Center': 29381.291883884493,
        'Fast Boundary': 29379.626579952484,
        'Middle Center': 29386.036402603575,
        'Middle Boundary': 29385.572688691390,
        'Slow Center': 29388.094197889477,
        'Slow Boundary': 29387.650660639003,
        'Extra 1 Center': 29379.156555620030,
        'Extra 1 Boundary': 29383.110733609470,
        'Extra 2 Center': 29419.451370044935,
        'Extra 2 Boundary': 29430.282915451247
    }

    print("\n" + "=" * 80)
    print(f"{'Curva':<18} | {'N':>4} | {'TradingView Live':>18} | {'Réplica Python':>18} | {'Error Absoluto':>14}")
    print("=" * 80)

    max_err = 0.0
    for name, (N, _) in lookbacks.items():
        tv_val = tv_real_last[name]
        py_val = simulated_clouds[name][299]
        err = abs(tv_val - py_val)
        if err > max_err:
            max_err = err
        print(f"{name:<18} | {N:4d} | {tv_val:18.8f} | {py_val:18.8f} | {err:14.2e}")

    print("-" * 80)
    print(f"Error máximo absoluto entre TradingView y réplica: {max_err:.4e} pts")

if __name__ == '__main__':
    run_replication()
