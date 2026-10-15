import master_cases

print("=== CHECKING MULTIPLIER C * (dt + 1) / 200 ACROSS ALL CASES ===")
print("Case                     | dt | Bars | C       | C * (dt + 1) / 200 | Ratio to Bars | Range")
for d in master_cases.dataset:
    dt = d['dt']
    bars = d['bars']
    c_val = d['C']
    factor = c_val * (dt + 1) / 200.0
    ratio_bars = factor / bars if bars > 0 else 0
    print(f"{d['s']}->{d['e']:8s} | {dt:2d} | {bars:4d} | {c_val:7.2f} | {factor:18.4f} | {ratio_bars:13.4f} | {d['range']:5.2f}")
