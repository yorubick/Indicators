import json
from pathlib import Path

p = Path("G:/trading/guias/analisis/Lite_Character_referencia.json")
if p.exists():
    with open(p, "r", encoding="utf-8") as f:
        print(json.dumps(json.load(f), indent=2)[:1000])

p2 = Path("G:/trading/guias/analisis/character_recent_15s.json")
if p2.exists():
    with open(p2, "r", encoding="utf-8") as f:
        print(json.dumps(json.load(f), indent=2)[:1000])
