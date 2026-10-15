import json
import pandas as pd
import numpy as np

# Load master cases
with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = [c for c in master['cases'] if c['bars'] >= 21 and c.get('C_Lite') is not None]

print("AUDITORÍA HONESTA Y DESPIADADA DE C PARA n >= 21:")
print(f"Total casos largos analizados: {len(cases)}")

# 1. Error puro de floor(n * dt / 18.3)
err_floor = [round(c['C_Lite']) - int(np.floor(c['bars'] * c['dt'] / 18.3)) for c in cases]
# 2. Error puro de round(n * dt / 18.3)
err_round = [round(c['C_Lite']) - int(round(c['bars'] * c['dt'] / 18.3)) for c in cases]
# 3. Error puro de floor(n * dt / 18.0)
err_18 = [round(c['C_Lite']) - int(np.floor(c['bars'] * c['dt'] / 18.0)) for c in cases]

print(f"\n1. Regla floor(n*dt / 18.3):")
print(f"   Aciertos exactos: {sum(e == 0 for e in err_floor)} / {len(cases)} ({sum(e == 0 for e in err_floor)/len(cases)*100:.1f}%)")
print(f"   MAE: {np.mean(np.abs(err_floor)):.2f} s")
print(f"   Error máximo: {max(np.abs(err_floor))} s")

print(f"\n2. Regla round(n*dt / 18.3):")
print(f"   Aciertos exactos: {sum(e == 0 for e in err_round)} / {len(cases)} ({sum(e == 0 for e in err_round)/len(cases)*100:.1f}%)")
print(f"   MAE: {np.mean(np.abs(err_round)):.2f} s")
print(f"   Error máximo: {max(np.abs(err_round))} s")

print(f"\n3. Regla floor(n*dt / 18.0):")
print(f"   Aciertos exactos: {sum(e == 0 for e in err_18)} / {len(cases)} ({sum(e == 0 for e in err_18)/len(cases)*100:.1f}%)")
print(f"   MAE: {np.mean(np.abs(err_18)):.2f} s")
print(f"   Error máximo: {max(np.abs(err_18))} s")

# Conclusion: None of these 1D rules solve C for n >= 21!
