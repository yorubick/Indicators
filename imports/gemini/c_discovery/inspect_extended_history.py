import pandas as pd

# Load the extended history file exported by Codex: manual/C_startSweep1920_geometria_historia_larga.csv
df = pd.read_csv(r'G:\trading\guias\analisis\manual\C_startSweep1920_geometria_historia_larga.csv')

# Convert time to datetime UTC
df['datetime'] = pd.to_datetime(df['time'], unit='s', utc=True)

# Filter between 18:30 and 19:00
df_sub = df[(df['datetime'] >= '2026-10-12 18:30:00') & (df['datetime'] <= '2026-10-12 19:00:00')].copy()

print(f"Total bars found: {len(df_sub)}")
print(df_sub[['datetime', 'open', 'high', 'low', 'close', 'Volume']].head(20).to_string(index=False))

# Look for major swing highs and swing lows between 18:30 and 19:00
high_bar = df_sub.loc[df_sub['high'].idxmax()]
low_bar = df_sub.loc[df_sub['low'].idxmin()]
print(f"\nHighest high in 18:30..19:00: {high_bar['high']} at {high_bar['datetime']}")
print(f"Lowest low in 18:30..19:00: {low_bar['low']} at {low_bar['datetime']}")
