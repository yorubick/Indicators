import re

with open(r'C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\PoiSzn_C_Deterministic_Lab_v4.pine', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in Pine: {len(lines)}")

# Let's check variables defined before line 164
defined_vars = set()
for i, line in enumerate(lines):
    # Match declarations like: var float x = ..., float x = ..., x = ...
    m = re.findall(r'\b(?:var\s+)?(?:float|int|bool|string)?\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(?::=|=)', line)
    for v in m:
        if v not in ['if', 'else', 'for', 'while']:
            defined_vars.add(v)
            
    # Check if 'ep' is in the line
    if 'ep' in re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', line):
        print(f"Line {i+1}: {line.strip()} (defined so far: {'ep' in defined_vars})")
