import json
import pandas as pd
import numpy as np

master = json.load(open("master_all_C_cases.json", encoding="utf-8"))
cases_60 = [c for c in master["cases"] if c["dt"] == 60 and c["bars"] == 21]

print("=== EVALUACIÓN DEL OPERADOR ARMÓNICO UNIFICADO (n=21) ===")
print(f"{'Caso ID':<28} | {'C_real':<6} | {'Div_Real':<8} | {'Ratio_N/span':<12} | {'Estado Detectado'}")
print("-" * 80)

for c in sorted(cases_60, key=lambda x: round(x["C"])):
    c_val = round(c["C"])
    T = 20 * 60 # 1200s
    div_real = T / c_val
    ratio_n = (24.0 * c_val / 60.0) / 20.0
    
    # Clasificación estructural adimensional
    df = pd.DataFrame(c["OHLCV"])
    h = df["high"].max()
    l = df["low"].min()
    rng = h - l
    c_end = df.iloc[-1]["close"]
    pos_c = (c_end - l) / rng if rng > 0 else 0.5
    
    ih = int(df["high"].argmax())
    il = int(df["low"].argmin())
    
    is_at_high = (ih >= 18) and (pos_c >= 0.85)
    is_at_low = (il >= 18) and (pos_c <= 0.15)
    
    print(f"{c['id']:<28} | {c_val:<6} | {div_real:<8.2f} | {ratio_n:<12.3f} | Pos={pos_c:.2f}, IdxH={ih}, IdxL={il}")
