import json
from pathlib import Path
import numpy as np

def load_cases():
    cases = []
    def load_from(path_str):
        p = Path(path_str)
        if not p.exists(): return []
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
        return [c for c in d.get("cases", []) if "OHLC" in c and "C" in c]
    cases += load_from("G:/trading/guias/analisis/C_matriz.json")
    cases += load_from("G:/trading/guias/analisis/C_START_regimenes.json")
    cases += load_from("G:/trading/guias/analisis/C_23_desplazamientos.json")
    return [c for c in cases if c.get("bars", len(c.get("OHLC", []))) >= 21]

cases = load_cases()

def analyze_case(c):
    ohlc = c["OHLC"]
    n = len(ohlc)
    opens = np.array([float(b["open"]) for b in ohlc])
    highs = np.array([float(b["high"]) for b in ohlc])
    lows = np.array([float(b["low"]) for b in ohlc])
    closes = np.array([float(b["close"]) for b in ohlc])
    
    # Extremes
    idx_max = int(np.argmax(highs))
    idx_min = int(np.argmin(lows))
    h_max = highs[idx_max]
    l_min = lows[idx_min]
    rng = h_max - l_min
    
    # Distance between extremes
    dist_ext = abs(idx_max - idx_min)
    
    # Bars from start to first extreme, and from last extreme to end
    first_ext = min(idx_max, idx_min)
    last_ext = max(idx_max, idx_min)
    bars_after_last_ext = (n - 1) - last_ext
    bars_before_first_ext = first_ext
    
    # Swings (simple 1-bar pivots: high > high[-1] and high > high[1])
    piv_h = [i for i in range(1, n - 1) if highs[i] > highs[i-1] and highs[i] > highs[i+1]]
    piv_l = [i for i in range(1, n - 1) if lows[i] < lows[i-1] and lows[i] < lows[i+1]]
    total_pivots = len(piv_h) + len(piv_l)
    
    # Efficiency ratio
    net_chg = abs(closes[-1] - opens[0])
    gross_chg = np.sum(np.abs(np.diff(closes)))
    er = net_chg / gross_chg if gross_chg > 0 else 0
    
    # Sum of ranges
    sum_ranges = np.sum(highs - lows)
    mean_range = sum_ranges / n
    
    c_val = c["C"]
    st = c.get("START", "")[11:16] if "T" in c.get("START", "") else c.get("START", "")[:5]
    en = c.get("END", "")[11:16] if "T" in c.get("END", "") else c.get("END", "")[:5]
    
    return {
        "start": st, "end": en, "n": n, "C": round(c_val, 2),
        "rng": rng, "dist_ext": dist_ext, "idx_max": idx_max, "idx_min": idx_min,
        "bars_after_last_ext": bars_after_last_ext,
        "bars_before_first_ext": bars_before_first_ext,
        "pivots": total_pivots, "er": round(er, 2),
        "mean_range": round(mean_range, 2)
    }

results = [analyze_case(c) for c in cases]

print(f"{'Case':14s} {'n':3s} {'C':6s} {'Rng':7s} {'DistExt':8s} {'MaxIdx':7s} {'MinIdx':7s} {'AfterExt':9s} {'BeforeExt':10s} {'Pivots':7s}")
for r in results:
    cs_name = f"{r['start']}-{r['end']}"
    print(f"{cs_name:14s} {r['n']:3d} {r['C']:6.1f} {r['rng']:7.2f} {r['dist_ext']:8d} {r['idx_max']:7d} {r['idx_min']:7d} {r['bars_after_last_ext']:9d} {r['bars_before_first_ext']:10d} {r['pivots']:7d}")
