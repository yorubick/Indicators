import csv, datetime
from pathlib import Path

# Load candles from G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv or from verified dataset
import json
with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

# Find any case that starts at 18:54 or 18:55
# Wait, let's look for the 1m candles of 18:50 to 19:20
p = Path('G:/trading/guias/analisis/seven_cloud_1m.csv')
if p.exists():
    with open(p) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    print("Found seven_cloud_1m.csv with", len(rows), "rows")
else:
    # search for 1m CSVs in G:/trading/guias/analisis/
    import glob
    csvs = glob.glob(r'G:\trading\guias\analisis\*1m*.csv')
    print("Found 1m csvs:", csvs[:5])
