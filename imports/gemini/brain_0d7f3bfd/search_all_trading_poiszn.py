import os, glob

search_terms = [b"Character Tree", b"PoiSzn", b"CCII", b"CSD", b"IDM", b"7Cloud"]

matches = []
for root, dirs, files in os.walk(r"G:\trading"):
    # skip large binary dirs or venvs if any
    if any(x in root for x in [".git", ".tools", "node_modules", "__pycache__"]):
        continue
    for f in files:
        if f.endswith(('.py', '.pine', '.txt', '.json', '.md')):
            p = os.path.join(root, f)
            try:
                with open(p, 'rb') as fp:
                    content = fp.read()
                    for term in search_terms:
                        if term in content:
                            matches.append((f, term.decode(), p))
                            break
            except Exception:
                pass

print(f"Total matching files: {len(matches)}")
for f, term, p in matches[:30]:
    print(f"{term:15s} | {f:30s} | {p}")
