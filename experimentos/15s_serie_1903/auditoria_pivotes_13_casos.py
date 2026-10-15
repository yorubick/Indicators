import csv
from datetime import datetime, timezone

with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# 13 consecutive cases START 19:03
cases = [
    ("19:23", 88, 50),
    ("19:24", 67, 52),
    ("19:25", 88, 71),
    ("19:26", 88, 135),
    ("19:27", 79, 130),
    ("19:28", 102, 88),
    ("19:29", 123, 135),
    ("19:30", 67, 112),
    ("19:31", 87, 112),
    ("19:32", 106, 112),
    ("19:33", 87, 112),
    ("19:34", 123, 136),
    ("19:35", 87, 112),
]

t_start = int(datetime(2026, 10, 12, 19, 3, 0, tzinfo=timezone.utc).timestamp())

print("=== AUDITORÍA CAUSAL DE PIVOTES Y ESTRUCTURA (19:23 a 19:35) ===")
print(f"{'END':<6} | {'C_15s':<5} | {'C_1m':<5} | {'High_prev':<9} | {'High_bar':<9} | {'Close_bar':<9} | {'New_High?':<10} | {'Wick_Up':<7} | {'Cl_Pos%':<7} | {'Clasificación Causal'}")
print("-" * 115)

# Causal state tracking up to END
for m_str, c_15, c_1m in cases:
    e_m = int(m_str.split(":")[1])
    t_end = int(datetime(2026, 10, 12, 19, e_m, 45, tzinfo=timezone.utc).timestamp())
    
    # All bars up to END
    bars_window = [bars_15s[t] for t in range(t_start, t_end + 1, 15)]
    bars_prior = bars_window[:-4] # prior bars before current 1m bar
    bars_current = bars_window[-4:] # 4 subbars of current 1m bar
    
    h_prior = max(float(b["high"]) for b in bars_prior)
    h_current = max(float(b["high"]) for b in bars_current)
    l_current = min(float(b["low"]) for b in bars_current)
    c_current = float(bars_current[-1]["close"])
    o_current = float(bars_current[0]["open"])
    
    rng = h_current - l_current
    wick_up = h_current - max(o_current, c_current)
    cl_pos = (c_current - l_current) / rng if rng > 0 else 0.5
    
    new_high = h_current > h_prior
    breakout = c_current > h_prior
    
    # Classification
    if breakout and cl_pos > 0.90 and wick_up <= 0.75:
        category = "IMPULSO / EXPANSION (Peak C)"
    elif new_high and wick_up > 1.5:
        category = "ABSORCION / RECHAZO (Meseta C)"
    elif not new_high and cl_pos > 0.75:
        category = "CONTINUACION INTERNA"
    elif not new_high:
        category = "CONTRACCION / RETROCESO"
    else:
        category = "TRANSICION"
        
    print(f"{m_str:<6} | {c_15:<5} | {c_1m:<5} | {h_prior:<9.2f} | {h_current:<9.2f} | {c_current:<9.2f} | {str(new_high):<10} | {wick_up:<7.2f} | {cl_pos*100:5.1f}% | {category}")
