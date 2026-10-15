import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases = {c["id"]: c for c in d["cases"]}

c_77 = cases["20261012_190100_192100_60s"]
c_50 = cases["20261012_190200_192200_60s"]

print("Case 19:01->19:21 (C=77):")
print("START bar:", c_77["OHLC"][0])
print("END bar:", c_77["OHLC"][-1])
highs_77 = [b["high"] for b in c_77["OHLC"]]
lows_77 = [b["low"] for b in c_77["OHLC"]]
print(f"Window High: {max(highs_77)} at bar {highs_77.index(max(highs_77))}")
print(f"Window Low: {min(lows_77)} at bar {lows_77.index(min(lows_77))}")

print("\nCase 19:02->19:22 (C=50):")
print("START bar:", c_50["OHLC"][0])
print("END bar:", c_50["OHLC"][-1])
highs_50 = [b["high"] for b in c_50["OHLC"]]
lows_50 = [b["low"] for b in c_50["OHLC"]]
print(f"Window High: {max(highs_50)} at bar {highs_50.index(max(highs_50))}")
print(f"Window Low: {min(lows_50)} at bar {lows_50.index(min(lows_50))}")

# Check what bar dropped off and what bar was added
dropped_bar = c_77["OHLC"][0] # 19:01
added_bar = c_50["OHLC"][-1]   # 19:22
print("\nDropped bar (19:01):", dropped_bar)
print("Added bar (19:22):", added_bar)
