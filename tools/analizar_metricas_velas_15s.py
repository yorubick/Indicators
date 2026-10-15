import csv
import json
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

rows = []
for end_str, c_val in cases_15s:
    m_offset = int(end_str.split(":")[1]) - 3
    t_end_m = t_start + m_offset * 60
    
    # 4 velas de 15s de este minuto
    sub_t = [t_end_m, t_end_m + 15, t_end_m + 30, t_end_m + 45]
    sub = [bars_15s[t] for t in sub_t if t in bars_15s]
    
    o = float(sub[0]["open"])
    c = float(sub[-1]["close"])
    h = max(float(b["high"]) for b in sub)
    l = min(float(b["low"]) for b in sub)
    rng = h - l
    body = c - o
    
    # Mechas de la vela de 1m
    upper_wick = h - max(o, c)
    lower_wick = min(o, c) - l
    
    # Última vela de 15s dentro del minuto
    last_15_o = float(sub[-1]["open"])
    last_15_c = float(sub[-1]["close"])
    last_15_h = float(sub[-1]["high"])
    last_15_l = float(sub[-1]["low"])
    last_15_body = last_15_c - last_15_o
    last_15_rng = last_15_h - last_15_l
    
    # Posición del cierre relativo a la vela
    cl_pos = (c - l) / rng if rng > 0 else 0.5
    
    rows.append({
        "END": end_str,
        "C": c_val,
        "Rng": rng,
        "Body": body,
        "UpWick": upper_wick,
        "LoWick": lower_wick,
        "UpWickRatio": round(upper_wick / rng, 2) if rng > 0 else 0,
        "BodyRatio": round(body / rng, 2) if rng > 0 else 0,
        "ClosePos": round(cl_pos, 2),
        "Last15_Body": last_15_body,
        "Last15_Rng": last_15_rng
    })

df = pd.DataFrame(rows)
print(df[["END", "C", "Rng", "Body", "UpWickRatio", "BodyRatio", "ClosePos", "Last15_Body", "Last15_Rng"]].to_string(index=False))
