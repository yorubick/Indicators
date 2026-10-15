import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = {c["id"]: c for c in d["cases"]}

c22 = cases["20261012_140000_142100_60s"]
c23 = cases["20261012_140000_142200_60s"]

print("=== Example 1: START 14:00 (C: 62 -> 83) ===")
highs_22 = [b["high"] for b in c22["OHLC"]]
lows_22 = [b["low"] for b in c22["OHLC"]]
max_h22 = max(highs_22)
min_l22 = min(lows_22)
print(f"Bars 1..22: High={max_h22}, Low={min_l22}, Range={max_h22 - min_l22}")

bar_23 = c23["OHLC"][-1]
print(f"Added Bar 23 (14:22): Open={bar_23['open']} High={bar_23['high']} Low={bar_23['low']} Close={bar_23['close']}")
print(f"Did Bar 23 make a NEW HIGH? {bar_23['high'] > max_h22} (High: {bar_23['high']} vs {max_h22})")
print(f"Did Bar 23 make a NEW LOW? {bar_23['low'] < min_l22} (Low: {bar_23['low']} vs {min_l22})")

c24 = cases["20261012_152700_155000_60s"]
c25 = cases["20261012_152700_155100_60s"]

print("\n=== Example 2: START 15:27 (C: 69 -> 93) ===")
highs_24 = [b["high"] for b in c24["OHLC"]]
lows_24 = [b["low"] for b in c24["OHLC"]]
max_h24 = max(highs_24)
min_l24 = min(lows_24)
print(f"Bars 1..24: High={max_h24}, Low={min_l24}, Range={max_h24 - min_l24}")

bar_25 = c25["OHLC"][-1]
print(f"Added Bar 25 (15:51): Open={bar_25['open']} High={bar_25['high']} Low={bar_25['low']} Close={bar_25['close']}")
print(f"Did Bar 25 make a NEW HIGH? {bar_25['high'] > max_h24} (High: {bar_25['high']} vs {max_h24})")
print(f"Did Bar 25 make a NEW LOW? {bar_25['low'] < min_l24} (Low: {bar_25['low']} vs {min_l24})")
