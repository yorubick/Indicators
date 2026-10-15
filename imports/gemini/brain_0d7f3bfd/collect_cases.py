import csv, json, datetime
from pathlib import Path
from obtener_C import recover

# Find all CSV files in G:/trading/guias/analisis
root = Path('G:/trading/guias/analisis')
all_csvs = sorted(root.glob('*.csv'))

# Load cases from JSON files if available
sens_15s = json.load(open(root / 'C_sensibilidad_15s.json', encoding='utf-8'))
barrido = json.load(open(root / 'C_barrido_ampliado.json', encoding='utf-8'))
agreg = json.load(open(root / 'C_agregacion.json', encoding='utf-8')) if (root / 'C_agregacion.json').exists() else {}

print(f"Total CSVs in dir: {len(all_csvs)}")

# Let's inspect the distinct cases
distinct_cases = []
# From barrido:
for c in barrido['cases']:
    distinct_cases.append({
        'START': c['START_UTC'],
        'END': '19:20:00',
        'dt': 15,
        'C': c['C'],
        'source': 'barrido_15s'
    })

# From agregacion
if agreg and 'cases' in agreg:
    for c in agreg['cases']:
        distinct_cases.append({
            'START': c['START_UTC'],
            'END': c.get('END_UTC', '19:21:30'),
            'dt': c['source_seconds'],
            'C': c['compatible_integer_C_seconds'][0],
            'source': 'agregacion'
        })

print(f"Total collected cases: {len(distinct_cases)}")
