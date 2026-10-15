"""
test_universal_operator_all_tf.py
==================================
Evaluación rigurosa del Operador Matemático Universal de C a través de todos los timeframes
(15s, 30s, 60s, 120s) y todas las duraciones de ventana en master_all_C_cases.json (179 casos).
"""

import json
import numpy as np
import pandas as pd

def evaluar():
    with open("master_all_C_cases.json", "r", encoding="utf-8") as f:
        master = json.load(f)

    cases = master["cases"]
    print(f"Total casos cargados: {len(cases)}")
    
    # Separar por timeframe
    by_tf = {}
    for c in cases:
        dt = c["dt"]
        by_tf.setdefault(dt, []).append(c)
        
    for dt, tf_cases in sorted(by_tf.items()):
        print(f"\n=======================================================")
        print(f" TIMEFRAME dt = {dt}s (Total: {len(tf_cases)} casos)")
        print(f"=======================================================")
        
        short = [c for c in tf_cases if c["bars"] < 21]
        long_cases = [c for c in tf_cases if c["bars"] >= 21]
        
        print(f"  - Régimen Corto (n < 21): {len(short)} casos")
        print(f"  - Régimen Largo (n >= 21): {len(long_cases)} casos")
        
        # 1. Evaluar Régimen Corto
        if short:
            res_short = []
            for c in short:
                n = c["bars"]
                T = n * dt
                c_obs = c["C"]
                # Fórmula exacta: max(dt, T / 18.3)
                c_pred = max(float(dt), (T * 10.0) / 183.0)
                res = abs(c_obs - c_pred)
                res_short.append(res)
            max_res = max(res_short)
            exact_pct = sum(1 for r in res_short if r < 1e-7) / len(res_short) * 100.0
            print(f"    [Corto] Exactos (< 1e-7): {exact_pct:.1f}% | Residuo Máx: {max_res:.2e}")
            
        # 2. Evaluar Régimen Largo
        if long_cases:
            int_res = []
            t_over_c = []
            base_diffs = []
            for c in long_cases:
                n = c["bars"]
                T = n * dt
                c_obs = c["C"]
                # Comprobar cuantización entera
                r_int = abs(c_obs - round(c_obs))
                int_res.append(r_int)
                t_over_c.append(T / c_obs)
                c_base = round(T / 18.3)
                base_diffs.append(round(c_obs) - c_base)
                
            max_int_res = max(int_res)
            int_exact_pct = sum(1 for r in int_res if r < 1e-7) / len(int_res) * 100.0
            median_toc = np.median(t_over_c)
            mean_toc = np.mean(t_over_c)
            std_toc = np.std(t_over_c)
            mean_base_err = np.mean(np.abs(base_diffs))
            
            exact_base_pct = sum(1 for d in base_diffs if d == 0) / len(base_diffs) * 100.0
            within_9s_pct = sum(1 for d in base_diffs if abs(d) <= 9) / len(base_diffs) * 100.0
            print(f"    [Largo] Entero Exacto (< 1e-7): {int_exact_pct:.1f}% | Residuo Máx Entero: {max_int_res:.2e}")
            print(f"    [Largo] Ratio T / C: Mediana = {median_toc:.3f} | Media = {mean_toc:.3f} | Std = {std_toc:.3f}")
            print(f"    [Largo] Coincidencia exacta con round(T/18.3): {exact_base_pct:.1f}% | Dentro de +/- 9s: {within_9s_pct:.1f}%")
            print(f"    [Largo] Error medio absoluto respecto a round(T/18.3): {mean_base_err:.2f} segundos")

if __name__ == "__main__":
    evaluar()
