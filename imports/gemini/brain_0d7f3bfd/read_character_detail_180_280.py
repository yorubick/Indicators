import json
from pathlib import Path

p = Path("G:/trading/guias/analisis/character_transcripcion_automatica.json")
with open(p, "r", encoding="utf-8") as f:
    items = json.load(f)

for it in items:
    if 180 <= it["start"] <= 280:
        print(f"[{it['start']:.1f}s - {it['end']:.1f}s]: {it['text']}")
