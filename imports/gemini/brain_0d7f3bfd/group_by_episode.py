import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Total training cases: {len(train)}")

# Let's see: what if we group training cases by episode?
episodes = {}
for c in train:
    st = c["START"][:13] # e.g. '2026-10-12T06', '2026-10-12T18', '2026-10-12T19'
    episodes.setdefault(st, []).append(c)

for ep, cases in episodes.items():
    print(f"\nEpisode: {ep} ({len(cases)} cases)")
    for c in cases:
        st_t = c["START"][11:16]
        en_t = c["END"][11:16]
        print(f"  {st_t}->{en_t} (n={c['bars']:2d}, dt={c['dt']:3d}) -> C = {round(c['C']):3d}")
