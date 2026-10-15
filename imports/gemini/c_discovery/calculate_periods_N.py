import json

with open("serie_1903_resueltos_15s.json", "r", encoding="utf-8") as f:
    cases_15s = json.load(f)

print(f"{'n':>2} | {'END':>5} | {'C_1m':>5} | {'N_1m':>6} | {'C_15s':>5} | {'N_15s':>6} | {'Ratio N15/N1m':>13} | {'C_1m/18.3':>9} | {'C_15/18.3':>9}")
print("-" * 80)

for c in cases_15s:
    n = c["n"]
    end = c["END"]
    c1m = c["C_1m"]
    c15 = c["C_15s_int"]
    
    # N = 24 * C / dt
    n1m = 24.0 * c1m / 60.0 # = 0.4 * c1m
    n15 = 24.0 * c15 / 15.0 # = 1.6 * c15
    
    ratio = n15 / n1m if n1m > 0 else 0
    print(f"{n:>2} | {end:>5} | {c1m:>5} | {n1m:>6.1f} | {c15:>5} | {n15:>6.1f} | {ratio:>13.2f} | {c1m/18.3:>9.2f} | {c15/18.3:>9.2f}")
