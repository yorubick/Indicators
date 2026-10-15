import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = {c["id"]: c for c in d["cases"]}

c41 = cases["20261012_044500_052500_60s"]
c46 = cases["20261012_044500_053000_60s"]

print("Case 41 (END 05:25): C =", c41["C_Lite"], "bars =", c41["bars"])
print("Case 46 (END 05:30): C =", c46["C_Lite"], "bars =", c46["bars"])

# Compare their OHLC
# Bars 41..46
print("Added bars 41 to 46:")
for i, b in enumerate(c46["OHLC"][40:], start=41):
    print(f"Bar {i}: time={b['time']} H={b['high']} L={b['low']} C={b['close']}")
