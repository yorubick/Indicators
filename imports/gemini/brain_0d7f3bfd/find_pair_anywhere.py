import csv, glob

all_files = glob.glob('G:/trading/guias/analisis/*.csv') + glob.glob('G:/trading/guias/analisis/manual/*.csv')

for f in all_files:
    try:
        with open(f, encoding='utf-8-sig') as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                l3a = row.get('Lane 3 A')
                l3b = row.get('Lane 3 B')
                if l3a and l3b:
                    try:
                        fa, fb = float(l3a), float(l3b)
                        if abs(fa - 30866.77) < 0.05 and abs(fb - 30866.63) < 0.05:
                            print(f"FOUND EXACT PAIR in {f} at time={row.get('time')}: Lane 3 A={fa}, Lane 3 B={fb}")
                    except ValueError:
                        pass
    except Exception:
        pass
print("Done.")
