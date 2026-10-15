import json
from pathlib import Path

# Load samples features
features_path = Path(r"C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\samples_features.json")
samples = json.loads(features_path.read_text())

print("=== CHECKING TICK-BASED FORMULAS ON ALL 50 SAMPLES ===")
print(f"{'ID':<15} {'TF':<3} {'Bars':<5} {'Rng':<6} {'Ticks':<6} {'C_meas':<7} {'T-21':<6} {'T+B':<6} {'T-B':<6}")
for s in sorted(samples, key=lambda x: (x['tf'], x['bars'], x['C'])):
    T = round(s['R'] * 4) # 0.25 mintick for NQ
    B = s['bars']
    C = s['C']
    print(f"{s['id']:<15} {s['tf']:<3d} {B:<5d} {s['R']:<6.2f} {T:<6d} {C:<7.1f} {T-21:<6d} {T+B:<6d} {T-B:<6d}")
