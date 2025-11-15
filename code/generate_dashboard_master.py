# generate_dashboard_master.py  (fixed)
import pandas as pd
from pathlib import Path

OUT = Path('outputs')
OUT.mkdir(parents=True, exist_ok=True)

# load final forecast (prefer complete file)
try:
    fc = pd.read_csv(OUT / "final_forecast_table_all_complete.csv")
except Exception:
    fc = pd.read_csv(OUT / "final_forecast_table_all.csv")

# load yearly ranking (this file has columns: Year,Technology,Avg_Interest)
rank = pd.read_csv(OUT / "tech_yearly_ranking.csv")
sent = pd.read_csv(OUT / "news_sentiment.csv")
ts = pd.read_csv(OUT / "trend_strength.csv")

# Build a per-technology yearly summary: take the most recent year's Avg_Interest per tech
# (safe approach: compute the mean or take the latest Year row)
# Here we'll compute the mean Avg_Interest per technology (robust)
if 'Avg_Interest' in rank.columns:
    latest_year = rank.groupby('Technology', as_index=False)['Avg_Interest'].mean()
    latest_year = latest_year.rename(columns={'Avg_Interest': 'Yearly_Avg_Interest'})
else:
    # fallback if column name differs
    # find any numeric column other than Year
    numeric_cols = [c for c in rank.columns if c not in ['Year', 'Technology']]
    if numeric_cols:
        col = numeric_cols[0]
        latest_year = rank.groupby('Technology', as_index=False)[col].mean().rename(columns={col:'Yearly_Avg_Interest'})
    else:
        # create empty placeholder
        latest_year = pd.DataFrame({'Technology': [], 'Yearly_Avg_Interest': []})

# Merge forecast + sentiment + trend strength
merged = fc.merge(sent, on='Technology', how='left').merge(ts, on='Technology', how='left')

# Merge the Yearly_Avg_Interest
merged = merged.merge(latest_year[['Technology','Yearly_Avg_Interest']], on='Technology', how='left')

out = OUT / 'dashboard_master.csv'
merged.to_csv(out, index=False)
print("Saved:", out)
print(merged.to_string(index=False))
