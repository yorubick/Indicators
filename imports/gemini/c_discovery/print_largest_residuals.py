import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = [c for c in d["cases"] if c.get("bars", 0) >= 21 and c.get("C_Lite") is not None]

ranked = []
for c in cases:
    n = c["bars"]
    dt = c["dt"]
    C_obs = round(c["C_Lite"])
    base = round((n * dt) / 18.3)
    res = C_obs - base
    ranked.append((abs(res), res, c["id"], dt, n, C_obs, base))

ranked.sort(reverse=True)

print("Top 20 Largest Residuals (C_obs - round(n * dt / 18.3)):")
for abs_r, res, cid, dt, n, c_obs, base in ranked[:20]:
    print(f"ID: {cid:28s} | dt={dt:2d}s n={n:3d} | C_obs={c_obs:3d} | Base={base:3d} | Residual = {res:+3d}")
