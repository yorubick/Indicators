import json
import re

for name in ["character_transcripcion_automatica.json", "auto_zoom_transcripcion_automatica.json"]:
    p = f"G:/trading/guias/analisis/{name}"
    with open(p, "r", encoding="utf-8") as f:
        items = json.load(f)
    print(f"\n==================== {name} ====================")
    for it in items:
        txt = it["text"]
        # look for any numbers or math terms
        if re.search(r'\b(72|89|24|16|60|61|183|10|18|21|22|23|25|77|71|62|68|81|82|83|93|cloud|multiplier|divide|multiply|scale|ratio|period|length|seconds|resolution)\b', txt, re.IGNORECASE):
            print(f"[{it['start']:.1f}s - {it['end']:.1f}s]: {txt}")
