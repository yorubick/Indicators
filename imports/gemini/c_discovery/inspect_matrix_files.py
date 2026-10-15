import json
import glob
from pathlib import Path

for path in glob.glob(r"G:\trading\guias\analisis\*matriz*.json"):
    print("Found matrix json:", path)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        print("  Keys:", list(data.keys())[:10])
        if "cases" in data:
            print(f"  cases count: {len(data['cases'])}")
            print("  First case:", data['cases'][0].get('id'), data['cases'][0].get('START'), data['cases'][0].get('END'), data['cases'][0].get('C'))
