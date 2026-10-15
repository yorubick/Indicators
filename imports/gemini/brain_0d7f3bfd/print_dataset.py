import master_cases

print(f"Total cases: {len(master_cases.dataset)}")
for d in master_cases.dataset:
    print(f"{d['s']} -> {d['e']} | dt={d['dt']:2d} | C={d['C']:3d} | bars={d['bars']:3d} | rng={d['range']:5.2f} | max={d['high']:8.2f} min={d['low']:8.2f}")
