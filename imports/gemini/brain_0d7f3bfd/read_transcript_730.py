import json

p = "G:/trading/guias/analisis/auto_zoom_transcripcion_automatica.json"
with open(p, "r", encoding="utf-8") as f:
    items = json.load(f)

for it in items:
    if 700 <= it["start"] <= 760:
        print(f"[{it['start']:.1f}s - {it['end']:.1f}s]: {it['text']}")
