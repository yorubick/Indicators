import json

with open('G:/trading/guias/analisis/caracteristicas_rangos.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
for item in data:
    print(f"{item['start']} to {item['end']} (dt={item['dt']}): bars={item['bars']}, C={item['C']}, height={item['height']}")
