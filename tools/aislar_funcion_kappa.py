import json
import pandas as pd
import numpy as np

master = json.load(open("master_all_C_cases.json", encoding="utf-8"))
cases = [c for c in master["cases"] if c["bars"] >= 21 and c.get("C_Lite") is not None]

rows = []
for c in cases:
    df = pd.DataFrame(c["OHLCV"])
    n = len(df)
    dt = c["dt"]
    T = (n - 1) * dt
    c_val = c["C_Lite"]
    
    # Factor kappa
    kappa = (24.0 * c_val) / T if T > 0 else 0
    divisor = 24.0 / kappa if kappa > 0 else 0
    
    # 1. Rango y Extremos
    highs = df["high"].values
    lows = df["low"].values
    closes = df["close"].values
    opens = df["open"].values
    
    r_high = highs.max()
    r_low = lows.min()
    rng = r_high - r_low
    
    idx_h = int(np.argmax(highs))
    idx_l = int(np.argmin(lows))
    
    bs_h = (n - 1) - idx_h
    bs_l = (n - 1) - idx_l
    dist_hl = abs(idx_h - idx_l)
    
    # 2. Ratios Adimensionales
    last_c = closes[-1]
    last_o = opens[-1]
    last_h = highs[-1]
    last_l = lows[-1]
    last_rng = last_h - last_l
    
    pos_range = (last_c - r_low) / rng if rng > 0 else 0.5
    dist_ext = min(pos_range, 1.0 - pos_range)
    
    net_disp = (last_c - opens[0]) / rng if rng > 0 else 0
    
    # Kaufman Efficiency Ratio (ER)
    path = np.sum(np.abs(np.diff(closes)))
    er = abs(last_c - opens[0]) / path if path > 0 else 0
    
    # Ratio de velas verdes
    green_ratio = np.mean(closes > opens)
    
    # Posición de la vela END
    end_body_norm = (last_c - last_o) / last_rng if last_rng > 0 else 0
    
    # ¿Es nuevo extremo en END?
    is_new_h = (idx_h == n - 1)
    is_new_l = (idx_l == n - 1)
    
    # Ubicación del swing relativo
    norm_bs_h = bs_h / (n - 1)
    norm_bs_l = bs_l / (n - 1)
    norm_dist_hl = dist_hl / (n - 1)
    
    rows.append({
        "id": c["id"],
        "dt": dt,
        "n": n,
        "T": T,
        "C": c_val,
        "kappa": round(kappa, 4),
        "divisor": round(divisor, 3),
        "pos_range": round(pos_range, 3),
        "dist_ext": round(dist_ext, 3),
        "net_disp": round(net_disp, 3),
        "er": round(er, 3),
        "green_ratio": round(green_ratio, 3),
        "norm_bs_h": round(norm_bs_h, 3),
        "norm_bs_l": round(norm_bs_l, 3),
        "norm_dist_hl": round(norm_dist_hl, 3),
        "is_new_h": 1 if is_new_h else 0,
        "is_new_l": 1 if is_new_l else 0
    })

df_feat = pd.DataFrame(rows)

print(f"Total casos analizados: {len(df_feat)}")
print("\n--- DISTRIBUCIÓN DE KAPPA ---")
print(df_feat["kappa"].describe())

print("\n--- CORRELACIONES DIRECTAS CON KAPPA ---")
corrs = df_feat.corr(numeric_only=True)["kappa"].sort_values(ascending=False)
print(corrs)
