import json
from pathlib import Path

p = Path("G:/trading/guias/analisis/Lite_0445_050300_1m_comparacion.json")
if p.exists():
    with open(p, "r", encoding="utf-8") as f:
        print(json.dumps(json.load(f), indent=2))
