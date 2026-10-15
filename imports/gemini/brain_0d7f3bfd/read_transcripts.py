import json
from pathlib import Path

for name in ["character_transcripcion_automatica.json", "auto_zoom_transcripcion_automatica.json"]:
    p = Path("G:/trading/guias/analisis") / name
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
        print(f"=== {name} ===")
        # if it's a dict or list
        if isinstance(d, dict):
            print("Keys:", list(d.keys()))
            for k in d:
                val = str(d[k])[:300]
                print(f"  {k}: {val}")
        elif isinstance(d, list):
            print("List length:", len(d))
            print("First item:", str(d[0])[:300])
