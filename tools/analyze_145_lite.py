import json
import math
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
with open(ROOT / "master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

cases = master.get("cases", [])
lite_cases = [c for c in cases if c.get("C_Lite") is not None]

print(f"Total cases analyzed: {len(lite_cases)}")

short_regime = []
long_regime = []

for c in lite_cases:
    dt = c.get("source_seconds") or c.get("dt")
    n = c.get("bars")
    c_val = c.get("C_Lite")

    if n < 21:
        # short regime
        pred = max(float(dt), float(n * dt * 10) / 183.0)
        res = abs(c_val - pred)
        short_regime.append({
            "id": c["id"],
            "n": n,
            "dt": dt,
            "C_obs": c_val,
            "C_pred": pred,
            "abs_err": res
        })
    else:
        # long regime
        T = n * dt
        base = round(T / 18.3)
        c_int = round(c_val)
        int_err = abs(c_val - c_int)
        dC = c_int - base
        k = dC / 9.0
        rem9 = dC % 9
        rem3 = dC % 3

        # OHLC features
        ohlc = c.get("OHLC", [])
        if ohlc:
            h_max = max(b["high"] for b in ohlc)
            l_min = min(b["low"] for b in ohlc)
            rng = h_max - l_min
            idx_h = [i for i, b in enumerate(ohlc) if b["high"] == h_max][0]
            idx_l = [i for i, b in enumerate(ohlc) if b["low"] == l_min][0]
            net_chg = ohlc[-1]["close"] - ohlc[0]["open"]
        else:
            h_max, l_min, rng, idx_h, idx_l, net_chg = [None]*6

        long_regime.append({
            "id": c["id"],
            "n": n,
            "dt": dt,
            "T": T,
            "C_obs": c_val,
            "C_int": c_int,
            "int_err": int_err,
            "base": base,
            "dC": dC,
            "k": k,
            "rem9": rem9,
            "rem3": rem3,
            "range": rng,
            "idx_h": idx_h,
            "idx_l": idx_l,
            "net_chg": net_chg,
            "start": c.get("START"),
            "end": c.get("END"),
        })

print("\n" + "="*80)
print(f"1. RÉGIMEN CORTO (n < 21 barras): {len(short_regime)} casos")
max_short_err = max(x["abs_err"] for x in short_regime) if short_regime else 0
print(f"Error máximo absoluto en n < 21 vs max(dt, n*dt*10/183): {max_short_err:.2e}")
print(f"Casos exactos con error < 1e-9: {sum(x['abs_err'] < 1e-9 for x in short_regime)} / {len(short_regime)}")

print("\n" + "="*80)
print(f"2. RÉGIMEN LARGO (n >= 21 barras): {len(long_regime)} casos")
max_int_err = max(x["int_err"] for x in long_regime)
print(f"Error máximo contra entero más cercano: {max_int_err:.2e}")
print(f"Casos estrictamente enteros (error < 1e-9): {sum(x['int_err'] < 1e-9 for x in long_regime)} / {len(long_regime)}")

k_dist = Counter(round(x["k"], 2) for x in long_regime)
print("\nDistribución de k = (C - Base) / 9:")
for k_val, count in sorted(k_dist.items()):
    pct = count / len(long_regime) * 100
    print(f"  k = {k_val:6.2f} : {count:4d} casos ({pct:5.1f}%)")

dC_dist = Counter(x["dC"] for x in long_regime)
print("\nDistribución de desviación dC = C - Base:")
for dc_val, count in sorted(dC_dist.items()):
    pct = count / len(long_regime) * 100
    print(f"  dC = {dc_val:4d} s : {count:4d} casos ({pct:5.1f}%)")

rem9_dist = Counter(x["rem9"] for x in long_regime)
print("\nDistribución de dC mod 9 (residuo de la celosía de base 9):")
for r, count in sorted(rem9_dist.items()):
    pct = count / len(long_regime) * 100
    print(f"  Residuo {r:2d} : {count:4d} casos ({pct:5.1f}%)")

rem3_dist = Counter(x["rem3"] for x in long_regime)
print("\nDistribución de dC mod 3 (residuo de la celosía de base 3):")
for r, count in sorted(rem3_dist.items()):
    pct = count / len(long_regime) * 100
    print(f"  Residuo {r:2d} : {count:4d} casos ({pct:5.1f}%)")

out_path = ROOT / "data" / "analisis_145_lite_casos.json"
out_data = {
    "total_cases": len(lite_cases),
    "short_cases": len(short_regime),
    "long_cases": len(long_regime),
    "short_regime_summary": {
        "formula": "C = max(dt, n * dt * 10 / 183)",
        "max_residual": max_short_err,
        "exact_count": sum(x['abs_err'] < 1e-9 for x in short_regime),
    },
    "long_regime_summary": {
        "base_formula": "round(T / 18.3)",
        "integer_residual": max_int_err,
        "k_distribution": {str(k): v for k, v in sorted(k_dist.items())},
        "dC_distribution": {str(dc): v for dc, v in sorted(dC_dist.items())},
        "mod9_distribution": {str(r): v for r, v in sorted(rem9_dist.items())},
        "mod3_distribution": {str(r): v for r, v in sorted(rem3_dist.items())},
    },
    "long_regime_cases": long_regime,
}
out_path.write_text(json.dumps(out_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"\nReporte guardado en: {out_path}")
