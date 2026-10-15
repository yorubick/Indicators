import json, sys
from pathlib import Path

# Add analysis directory to sys.path
sys.path.insert(0, 'G:/trading/guias/analisis')
from obtener_C import recover

manual_dir = Path('G:/trading/guias/analisis/manual')
csv_files = sorted(manual_dir.glob('*.csv'))

print(f"Total CSVs in manual: {len(csv_files)}")
results = []
errors = []

for p in csv_files:
    try:
        res = recover(p)
        results.append({
            'file': p.name,
            'dt': res['source_seconds'],
            'C_int': res['compatible_integer_C_seconds'],
            'interval': res['C_seconds_interval'],
            'periods': res['periods'],
            'pairs': res['pairs_per_curve'],
            'max_rmse': res['max_rmse_step']
        })
    except Exception as e:
        errors.append((p.name, str(e)))

print("\n=== SUCCESSFUL EXTRACTIONS ===")
for r in results:
    interv = r['interval']
    low = interv['lower_inclusive']
    high = interv['upper_exclusive']
    print(f"{r['file']:35s} | dt={r['dt']:3d} | C={str(r['C_int']):6s} | [{low:.4f}, {high:.4f}) | Extra1={r['periods'].get('Extra cloud 1')}/{r['periods'].get('Extra cloud 1 boundary')}")

if errors:
    print("\n=== ERRORS / FAILED EXTRACTIONS ===")
    for fname, err in errors:
        print(f"{fname:35s} | {err}")
