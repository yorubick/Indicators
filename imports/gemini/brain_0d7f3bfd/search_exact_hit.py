import csv, glob
from datetime import datetime, timezone

t_target = 1760300000 # Let's find exact timestamp for 2026-10-12 19:26:45 UTC
t_exact = int(datetime.fromisoformat('2026-10-12T19:26:45+00:00').timestamp())

print(f"Target timestamp: {t_exact}")

all_files = glob.glob('G:/trading/guias/analisis/*.csv') + glob.glob('G:/trading/guias/analisis/manual/*.csv')

for f in all_files:
    try:
        with open(f, encoding='utf-8-sig') as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                if int(row.get('time', 0)) == t_exact:
                    # Check any column with 30866.77 or 30866.63
                    for k, v in row.items():
                        if v and ('30866.77' in v or '30866.63' in v):
                            print(f"EXACT HIT: {f} | col '{k}' = {v}")
    except Exception:
        pass
