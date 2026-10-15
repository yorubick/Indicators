with open(r'C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\PoiSzn_C_Deterministic_Lab_v4.pine', encoding='utf-8') as f:
    code = f.read()

# Let's inspect the exact lines 105 to 125
lines = code.splitlines()
for i in range(104, 125):
    print(f"{i+1}: {lines[i]}")
