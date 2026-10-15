import json
from pathlib import Path

for name in ["character_transcripcion_automatica.json", "auto_zoom_transcripcion_automatica.json"]:
    p = Path("G:/trading/guias/analisis") / name
    with open(p, "r", encoding="utf-8") as f:
        items = json.load(f)
    print(f"\n==================== {name} ====================")
    full_text = " ".join(it["text"] for it in items)
    # Search for sentences mentioning key terms
    keywords = ["length", "period", "calculate", "formula", "ema", "cloud", "range", "box", "zoom", "manual", "auto", "swing", "tree", "anchor", "time"]
    for it in items:
        txt = it["text"]
        if any(w in txt.lower() for w in ["length", "period", "calculat", "formula", "cloud", "origin", "tree", "zoom", "anchor", "profile"]):
            print(f"[{it['start']:.1f}s - {it['end']:.1f}s]: {txt}")
