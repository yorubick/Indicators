import pandas as pd

df = pd.read_csv(r'G:\trading\guias\analisis\manual\C_source15_chart15_b.csv')
# Look at rows around 19:03:15
df_sub = df[(df['time'] >= 1791831780) & (df['time'] <= 1791831840)]
# Let's inspect by timestamp or datetime
print("Columns in file:", df.columns[:10])
print(df.head(5))
