import json
import pandas as pd
import numpy as np

master = json.load(open("master_all_C_cases.json", encoding="utf-8"))
cases_60 = [c for c in master["cases"] if c["dt"] == 60 and c["bars"] == 21]

groups = {
    "-2 (C=50)": ["20261012_190200_192200_60s", "20261012_190300_192300_60s", "20261012_190400_192400_60s"],
    "-1 (C=62)": ["20261012_140000_142000_60s", "20261012_140100_142100_60s"],
    " 0 (C=68-69)": ["20261012_153000_155000_60s", "20261012_153100_155100_60s", "20261013_153300_155300_60s"],
    "+1 (C=75-80)": ["20261012_060000_062000_60s", "20261012_190000_192000_60s", "20261012_190100_192100_60s", "20261012_044500_050500_60s"],
    "+2 (C=87)": ["20261013_062500_064500_60s"]
}

print("=== COMPARACIÓN ESTRUCTURAL ENTRE LOS 5 GRUPOS ARMÓNICOS ===")
for g_name, case_ids in groups.items():
    print(f"\n--- GRUPO k = {g_name} ---")
    for cid in case_ids:
        c = [x for x in cases_60 if x["id"] == cid][0]
        df = pd.DataFrame(c["OHLCV"])
        
        # Extremos
        h = df["high"].max()
        l = df["low"].min()
        rng = h - l
        
        # Desplazamiento neto
        c_start = df.iloc[0]["open"]
        c_end = df.iloc[-1]["close"]
        disp = c_end - c_start
        disp_norm = disp / rng if rng > 0 else 0
        
        # Posición de cierre en rango
        pos_close = (c_end - l) / rng if rng > 0 else 0.5
        
        # Ubicación temporal del pico máximo y mínimo
        ih = int(df["high"].argmax())
        il = int(df["low"].argmin())
        
        # Número de giros/pivotes locales (radio 1)
        piv_h = sum(1 for i in range(1, len(df)-1) if df.iloc[i]["high"] > df.iloc[i-1]["high"] and df.iloc[i]["high"] >= df.iloc[i+1]["high"])
        piv_l = sum(1 for i in range(1, len(df)-1) if df.iloc[i]["low"] < df.iloc[i-1]["low"] and df.iloc[i]["low"] <= df.iloc[i+1]["low"])
        
        # Última vela (END)
        end_body = df.iloc[-1]["close"] - df.iloc[-1]["open"]
        end_rng = df.iloc[-1]["high"] - df.iloc[-1]["low"]
        
        print(f"{cid:<28} | C={round(c['C']):<2} | DispNorm={disp_norm:+5.2f} | PosClose={pos_close:4.2f} | IdxH={ih:2d} | IdxL={il:2d} | PivH={piv_h} | PivL={piv_l} | EndBody={end_body:+5.2f} | Rng={rng:5.2f}")
