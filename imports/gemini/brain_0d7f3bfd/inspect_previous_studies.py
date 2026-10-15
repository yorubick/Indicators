import json
from pathlib import Path

names = [
    "C_balance_recorrido.json",
    "C_contacto_convergencia.json",
    "C_contacto_interior.json",
    "C_orden_direccion.json",
    "C_limites_y_mecha.json",
    "estudio_rangos.json",
    "ajuste_emas.json"
]

for name in names:
    p = Path("G:/trading/guias/analisis") / name
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
        print(f"\n=== {name} ===")
        if isinstance(d, dict):
            print("Keys:", list(d.keys())[:10])
            for k in list(d.keys())[:5]:
                v = str(d[k])[:150]
                print(f"  {k}: {v}")
        elif isinstance(d, list):
            print("List len:", len(d))
            if d:
                print("First item:", str(d[0])[:200])
