import json, glob
from pathlib import Path

# Load master cases
import sys
sys.path.append(r"C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch")
from master_cases import load_master_cases

cases = load_master_cases()
print(f"Total master cases: {len(cases)}")

# Print all cases with their metadata
print(f"{'ID':<15} {'Day':<12} {'TF':<5} {'Bars':<5} {'C':<10} {'Start':<20} {'End':<20}")
for c in sorted(cases, key=lambda x: (x.timeframe, x.bars if x.bars else 0, x.C)):
    print(f"{c.case_id:<15} {c.day:<12} {c.timeframe:<5} {str(c.bars):<5} {c.C:<10.2f} {c.start_time:<20} {c.end_time:<20}")
