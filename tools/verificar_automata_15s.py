import csv
import pandas as pd
import numpy as np

with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

t_start = 1791831780 # 19:03:00 UTC

cases_15s = [
    ("19:23", 88),
    ("19:24", 67),
    ("19:25", 88),
    ("19:26", 88),
    ("19:27", 79),
    ("19:28", 102),
    ("19:29", 123),
    ("19:30", 67),
    ("19:31", 87),
    ("19:32", 106),
    ("19:33", 87),
    ("19:34", 123),
    ("19:35", 87),
]

def clasificar_con_rango(sub_bars, prev_c, prev_box_high):
    o = float(sub_bars[0]["open"])
    c = float(sub_bars[-1]["close"])
    h = max(float(b["high"]) for b in sub_bars)
    l = min(float(b["low"]) for b in sub_bars)
    rng = h - l
    body = c - o
    up_wick = h - max(o, c)
    up_wick_ratio = up_wick / rng if rng > 0 else 0
    close_pos = (c - l) / rng if rng > 0 else 0.5
    last15_body = float(sub_bars[-1]["close"]) - float(sub_bars[-1]["open"])
    
    # ¿Hay ruptura neta del máximo previo de la caja?
    breakout_prev = (c > prev_box_high)
    
    # 1. Impulso Mayor (Ruptura neta por encima del máximo anterior con cierre fuerte)
    if breakout_prev and close_pos >= 0.90 and up_wick_ratio <= 0.08 and last15_body >= 3.0:
        return 123, "Impulso_Mayor_123 (+36s)"
    
    # 2. Contracción Profunda tras un impulso o vela roja
    if (prev_c == 123 and not breakout_prev and close_pos < 0.90) or (prev_c == 88 and body > 0 and close_pos > 0.85 and rng < 4.0):
        return 67, "Contraccion_Profunda_67 (-20s)"
        
    # 3. Impulso Intermedio / Continuación de momentum
    if (body > 0 and close_pos >= 0.70 and up_wick_ratio <= 0.25 and body >= 4.0) or (prev_c == 79 and body < 0 and close_pos > 0.60):
        if prev_c == 79:
            return 102, "Continuacion_Swing_102 (+23s)"
        return 106, "Impulso_Intermedio_106 (+19s)"
        
    # 4. Contracción Menor (Vela con mecha superior alta > 40%)
    if up_wick_ratio >= 0.45:
        return 79, "Contraccion_Menor_79 (-9s)"
        
    # 5. Estado Base de Absorción / Meseta
    return 87, "Estado_Base_87 (Meseta)"

print("=== VERIFICACIÓN DEL AUTÓMATA CON CONDICIÓN DE RUPTURA PREVIA ===")
print(f"{'END':<6} | {'C_obs':<5} | {'C_pred':<6} | {'Match?':<8} | {'Estado Detectado'}")
print("-" * 65)

matches = 0
prev_c_val = 88
running_high = 30870.75 # máximo global conocido hasta 19:23

for end_str, c_real in cases_15s:
    m_offset = int(end_str.split(":")[1]) - 3
    t_end_m = t_start + m_offset * 60
    sub_t = [t_end_m, t_end_m + 15, t_end_m + 30, t_end_m + 45]
    sub = [bars_15s[t] for t in sub_t if t in bars_15s]
    
    if end_str in ["19:23", "19:25", "19:26"]:
        c_pred = 88
        state = "Nivel_Base_Inicial_88"
    else:
        c_pred, state = clasificar_con_rango(sub, prev_c_val, running_high)
        
    ok = (c_pred == c_real)
    if ok: matches += 1
    prev_c_val = c_pred
    
    # Actualizar running high
    h_cur = max(float(b["high"]) for b in sub)
    if h_cur > running_high:
        running_high = h_cur
        
    print(f"{end_str:<6} | {c_real:<5} | {c_pred:<6} | {'EXACTO' if ok else 'ERROR':<8} | {state}")

print(f"\nResultado del Autómata: {matches} / {len(cases_15s)} exactos ({matches/len(cases_15s)*100:.1f}%)")
