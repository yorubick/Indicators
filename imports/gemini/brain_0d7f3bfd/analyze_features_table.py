import json
from pathlib import Path
import numpy as np

# Load samples features
features_path = Path(r"C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\samples_features.json")
samples = json.loads(features_path.read_text())

# Print table of C values vs features
print("=== SAMPLE OVERVIEW ===")
print(f"{'TF':<3} {'START':<9} {'END':<9} {'Bars':<5} {'C':<6} {'Rng':<6} {'b_H':<4} {'b_L':<4} {'Retrace':<8} {'Move':<8} {'R/ATR':<6}")
for s in sorted(samples, key=lambda x: (x['tf'], x['C'], x['bars'])):
    print(f"{s['tf']:<3d} {s['s']:<9} {s['e']:<9} {s['bars']:<5d} {s['C']:<6.1f} {s['R']:<6.2f} {s['bars_since_H']:<4d} {s['bars_since_L']:<4d} {s['retrace']:<8.3f} {s['move']:<8.3f} {s['r_atr']:<6.2f}")
