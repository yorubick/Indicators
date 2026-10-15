import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = [c for c in d["cases"] if c.get("bars", 0) >= 21 and c.get("C_Lite") is not None]

# Test harmonic decomposition:
# Can residual res = C - round(n * dt / 18.3) be represented as k * 27 or k * 9 or k * 3?
res_all = []
for c in cases:
    n = c["bars"]
    dt = c["dt"]
    C_obs = round(c["C_Lite"])
    base = round((n * dt) / 18.3)
    res = C_obs - base
    res_all.append((c["id"], dt, n, C_obs, base, res))

print(f"Total long cases: {len(res_all)}")

# Check residuals mod 9, mod 27, mod 3
within_2 = sum(1 for r in res_all if abs(r[5]) <= 2)
within_5 = sum(1 for r in res_all if abs(r[5]) <= 5)

print(f"Cases with |Residual| <= 2: {within_2} / {len(res_all)} ({within_2/len(res_all)*100:.1f}%)")
print(f"Cases with |Residual| <= 5: {within_5} / {len(res_all)} ({within_5/len(res_all)*100:.1f}%)")

# Check if residual is close to {0, +-9, +-18, +-27, +-36, +-45, +-54, +-72}
harmonic_lattice = [0, 9, -9, 18, -18, 27, -27, 36, -36, 45, -45, 54, -54, 72, -72]

matches_lattice_tol1 = 0
matches_lattice_tol2 = 0
for r in res_all:
    res = r[5]
    dist = min(abs(res - h) for h in harmonic_lattice)
    if dist <= 1:
        matches_lattice_tol1 += 1
    if dist <= 2:
        matches_lattice_tol2 += 1

print(f"Residual within +-1 of lattice {0, +-9, +-18, +-27, +-45, +-72}: {matches_lattice_tol1} / {len(res_all)} ({matches_lattice_tol1/len(res_all)*100:.1f}%)")
print(f"Residual within +-2 of lattice {0, +-9, +-18, +-27, +-45, +-72}: {matches_lattice_tol2} / {len(res_all)} ({matches_lattice_tol2/len(res_all)*100:.1f}%)")
