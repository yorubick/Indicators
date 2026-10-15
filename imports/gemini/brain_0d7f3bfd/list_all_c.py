import os, re

vals = set()
for root, dirs, files in os.walk('G:/trading/guias/analisis'):
    for f in files:
        if f.endswith('.json'):
            try:
                p = os.path.join(root, f)
                text = open(p, encoding='utf-8', errors='ignore').read()
                for m in re.finditer(r'"C(_compatible|_entero)?":\s*(\d+)', text):
                    vals.add(int(m.group(2)))
            except:
                pass

print("All unique integer C found:", sorted(list(vals)))
