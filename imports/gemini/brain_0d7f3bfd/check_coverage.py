import csv, datetime
from pathlib import Path

ref_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows = list(csv.DictReader(ref_path.open(encoding='utf-8-sig')))

# Let's also check if there is an earlier file that covers from 18:50
ref_early = Path('G:/trading/guias/analisis/C_end1920_start1850_chart.csv')
if ref_early.exists():
    rows_early = list(csv.DictReader(ref_early.open(encoding='utf-8-sig')))
    print(f"Early file has {len(rows_early)} rows, first time: {rows_early[0]['time']}, last: {rows_early[-1]['time']}")

print(f"Barrido file has {len(rows)} rows, first time: {rows[0]['time']}, last: {rows[-1]['time']}")
