import pandas as pd
from pathlib import Path

csvs = list(Path("G:/trading/guias/analisis/manual").glob("*.csv"))

print(f"Scanning delivery active columns across {len(csvs)} files:")
found = 0
for p in csvs[:30]:
    df = pd.read_csv(p)
    if "Bull delivery active" in df.columns:
        bull_sum = df["Bull delivery active"].astype(float).sum()
        bear_sum = df["Bear delivery active"].astype(float).sum()
        if bull_sum > 0 or bear_sum > 0:
            print(f"{p.name}: Bull={bull_sum}, Bear={bear_sum}")
            found += 1

print(f"Found non-zero delivery in {found} files out of 30.")
