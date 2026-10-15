import json
from pathlib import Path

p = Path("G:/trading/guias/analisis/auto_zoom_transcripcion_automatica.json")
with open(p, "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Searching {len(items)} segments in auto_zoom:")
for it in items:
    txt = it["text"]
    if any(k in txt.lower() for k in ["anchor", "character", "tree", "extreme", "zoom", "move", "cloud", "range"]):
        print(f"[{it['start']:.1f}s - {it['end']:.1f}s]: {txt}")
