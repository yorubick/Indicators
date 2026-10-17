"""Recupera C de las exportaciones de M9 (manual/M9_*.csv) y lo compara con las
predicciones registradas en M9_ventanas.json antes de medir."""
import json, sys, subprocess, re
from pathlib import Path
AQUI = Path(__file__).parent; RAIZ = AQUI.parents[1]
reg = json.loads((AQUI / "M9_ventanas.json").read_text())["ventanas"]
aciertos, medidos = {}, 0
for v in reg:
    csv = RAIZ / "manual" / v["archivo"]
    if not csv.exists():
        print(f"{v['id']} {v['archivo']}: falta"); continue
    out = subprocess.run([sys.executable, str(RAIZ / "tools/invertir_C_csv.py"), str(csv)], capture_output=True, text=True).stdout
    m = re.search(r"C mediana = ([\d.]+) \(mín ([\d.]+), máx ([\d.]+)\)", out)
    if not m:
        print(f"{v['id']}: no se pudo recuperar C\n{out}"); continue
    C = float(m.group(1)); medidos += 1
    print(f"{v['id']} {v['START']}→{v['END'][11:]} n={v['n']:<3} C={C:<9} " + "  ".join(f"{k}={p:g}{'✓' if round(p) == round(C) else ''}" for k, p in v["predicciones"].items()))
    for k, p in v["predicciones"].items():
        aciertos[k] = aciertos.get(k, 0) + (round(p) == round(C))
print(f"\nmedidos {medidos}/30; aciertos por regla:", aciertos)
