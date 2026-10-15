import json
import pandas as pd
import numpy as np

def run_joint_audit():
    # 1. Cargar casos 2m
    c2m_data = json.load(open('data/ohlcv_2m_1430_1516.json'))
    df_2m = pd.DataFrame(c2m_data)
    
    cases_2m = [
        {'id': '2m_1510', 'dt': 120, 'n': 21, 'C': 124, 'sub': df_2m.iloc[:21]},
        {'id': '2m_1512', 'dt': 120, 'n': 22, 'C': 153, 'sub': df_2m.iloc[:22]},
        {'id': '2m_1514', 'dt': 120, 'n': 23, 'C': 146, 'sub': df_2m.iloc[:23]},
        {'id': '2m_1516', 'dt': 120, 'n': 24, 'C': 190, 'sub': df_2m.iloc[:24]}
    ]
    
    # 2. Cargar casos 15s sweep
    sweep_15s = json.load(open('data/barrido_start_1933.json'))
    cases_15s_raw = sweep_15s['cases']
    df_15s = pd.read_csv('data/exports/20261012_start_191400_end_193300_15s.csv')
    df_15s['dt_utc'] = pd.to_datetime(df_15s['time'], unit='s', utc=True)
    
    cases_15s = []
    end_utc = '2026-10-12 19:33:00+00:00'
    for c in cases_15s_raw:
        s_utc = c['START'].replace('Z', '+00:00')
        c_val = round(c['C_resuelto'])
        mask = (df_15s['dt_utc'] >= s_utc) & (df_15s['dt_utc'] <= end_utc)
        sub = df_15s[mask].reset_index(drop=True)
        cases_15s.append({
            'id': c['case_id'],
            'dt': 15,
            'n': len(sub),
            'C': c_val,
            'sub': sub
        })
        
    all_cases = cases_2m + cases_15s
    print(f"Total casos consolidados para búsqueda causal: {len(all_cases)} (4 de 2m + 15 de 15s)")
    
    # 3. Extraer métricas universales normalizadas
    dataset = []
    for item in all_cases:
        sub = item['sub']
        n = item['n']
        dt = item['dt']
        T_inc = n * dt
        C = item['C']
        
        gh = sub['high'].max()
        gl = sub['low'].min()
        tot_rng = gh - gl
        
        last_c = sub.iloc[-1]['close']
        last_o = sub.iloc[-1]['open']
        last_h = sub.iloc[-1]['high']
        last_l = sub.iloc[-1]['low']
        
        # Posición de cierre relativo
        cl_pos = (last_c - gl) / tot_rng if tot_rng > 0 else 0.5
        dist_ext = min(last_c - gl, gh - last_c) / tot_rng if tot_rng > 0 else 0
        
        # Base macro
        c_base = round((T_inc * 10.0) / 183.0)
        delta_c = C - c_base
        k_harmonic = delta_c / 9.0
        
        # Ratio de escala C / T
        ratio_tc = T_inc / C
        
        # Ratios de precio
        net_travel = abs(last_c - sub.iloc[0]['open'])
        diffs = np.abs(np.diff(sub['close']))
        path = np.sum(diffs)
        er = net_travel / path if path > 0 else 0
        
        # Volatilidad relativa (Rango / T_inc)
        speed = tot_rng / T_inc
        
        dataset.append({
            'id': item['id'],
            'dt': dt,
            'n': n,
            'T_inc': T_inc,
            'C': C,
            'C_base': c_base,
            'Delta_C': delta_c,
            'k_harm': round(k_harmonic, 2),
            'Ratio_TC': round(ratio_tc, 2),
            'Range': tot_rng,
            'ClosePos': round(cl_pos, 3),
            'DistExt': round(dist_ext, 3),
            'ER': round(er, 3),
            'Speed': round(speed, 4)
        })
        
    df_all = pd.DataFrame(dataset)
    print("\n=== TABLA DE AUDITORÍA CRUZADA MULTI-TIMEFRAME (15S & 2M) ===")
    print(df_all[['id', 'dt', 'n', 'T_inc', 'C', 'C_base', 'Delta_C', 'k_harm', 'Ratio_TC', 'Range', 'ClosePos', 'ER']].to_string(index=False))

if __name__ == '__main__':
    run_joint_audit()
