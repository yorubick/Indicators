import csv, glob

t_exact = 1791833205 # 2026-10-12 19:26:45 UTC

all_files = glob.glob('G:/trading/guias/analisis/*.csv') + glob.glob('G:/trading/guias/analisis/manual/*.csv')

print(f"Scanning {len(all_files)} files at time={t_exact}...")
for f in all_files:
    try:
        with open(f, encoding='utf-8-sig') as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                if int(row.get('time', 0)) == t_exact:
                    for k, v in row.items():
                        if v:
                            try:
                                fv = float(v)
                                if abs(fv - 30866.77) < 0.05:
                                    print(f"HIT L3A ~ 30866.77: {f} | {k} = {fv}")
                                if abs(fv - 30866.63) < 0.05:
                                    print(f"HIT L3B ~ 30866.63: {f} | {k} = {fv}")
                            except ValueError:
                                pass
    except Exception:
        pass
print("Scan complete.")
