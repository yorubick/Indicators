import json
import pandas as pd
import numpy as np

# Load all 112 rows from Gemini_v31_auditoria.json
with open(r'G:\trading\guias\analisis\Gemini_v31_auditoria.json') as f:
    aud = json.load(f)

rows = aud['rows']

# Filter the 13 additional cases
add_cases = rows[99:]

print("=== INSPECTING THE 13 ADDITIONAL CONTROLS ===")
for r in add_cases:
    # compute features
    # we need the ohlc from the original files
    print(f"ID: {r['id']} | dt={r['dt']} | bars={r['bars']} | actual_C={r['C']}")
