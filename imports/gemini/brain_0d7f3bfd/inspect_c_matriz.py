import json
from pathlib import Path

matriz_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
data = json.loads(matriz_path.read_text(encoding='utf-8'))

print(f"Total cases in C_matriz: {len(data['cases'])}")
print(f"Scope: {data.get('scope')}")
print("Predeclared predictions:")
for p in data.get('predeclared_count_predictions', []):
    print(" ", p)

print("\n--- ALL CASES IN C_MATRIZ ---")
print(f"{'START':<10} {'END':<10} {'Bars':<6} {'C':<12} {'High':<10} {'Low':<10} {'Range':<8} {'LastClose':<10}")
for c in sorted(data['cases'], key=lambda x: (x['START'], x['END'])):
    rng = c['high'] - c['low']
    lc = c['last_OHLC']['close']
    c_val = f"{c['C']:.4f}" if isinstance(c['C'], float) else str(c['C'])
    print(f"{c['START']:<10} {c['END']:<10} {c['bars']:<6} {c_val:<12} {c['high']:<10.2f} {c['low']:<10.2f} {rng:<8.2f} {lc:<10.2f}")
