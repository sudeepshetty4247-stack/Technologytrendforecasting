# generate_yearly_ranking.py
import pandas as pd
from pathlib import Path

df = pd.read_csv("data/trends_processed.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

ranking = df.groupby(['Year','Technology'])['Interest'].mean().reset_index().rename(columns={'Interest':'Avg_Interest'})
ranking = ranking.sort_values(['Year','Avg_Interest'], ascending=[True, False])
out = Path('outputs/tech_yearly_ranking.csv')
out.parent.mkdir(parents=True, exist_ok=True)
ranking.to_csv(out, index=False)
print("Saved:", out)
print(ranking.head(10).to_string(index=False))
